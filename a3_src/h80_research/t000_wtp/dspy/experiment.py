# -*- coding: utf-8 -*-
"""
"""


import collections
import itertools
import os

import openai

import dspy
import dspy.primitives
import dspy.teleprompt
import joblib
import matplotlib
import ruamel.yaml
import seaborn

import key



# -----------------------------------------------------------------------------
def main():
    """
    """

    print('HELLO3')



# -----------------------------------------------------------------------------
def _backup():


    list_example = _generate_list_example()

    model = _language_model('gpt-4-turbo-preview')
    dspy.settings.configure(lm             = model,
                            bypass_suggest = True)

    predict_is_supporting = ModuleIsSupporting(num_samples = 10)

    # model.inspect_history(n = 10)
    # predict_is_supporting.save('20240301_predict_is_supporting_gpt-3.5-turbo.json')

    # BASELINE
    #
    print('=' * 80)
    print('=' * 80)
    list_metric = list()
    for example in list_example:
        prediction = predict_is_supporting(
                                first_statement  = example.first_statement,
                                second_statement = example.second_statement)
        metric = _metric_is_supporting_consistency(None, prediction)
        list_metric.append(metric)
    model.inspect_history(n = 10)
    plot_histogram(list_metric)
    print('=' * 80)
    print('=' * 80)

    # optimise_for_consistency = dspy.teleprompt.SignatureOptimizer(
    #                                 metric = _metric_is_supporting_consistency)

    # eval_kwargs = dict(num_threads      = 64,
    #                    display_progress = True,
    #                    display_table    = 0)
    # predict_is_supporting_opt = optimise_for_consistency.compile(
    #                                     student     = predict_is_supporting,
    #                                     devset      = list_example,
    #                                     eval_kwargs = eval_kwargs)

    # model.inspect_history(n = 10)
    # # predict_is_supporting_opt.save('20240301_predict_is_supporting_opt_gpt-3.5-turbo.json')

    # # BASELINE
    # #
    # print('=' * 80)
    # print('=' * 80)
    # list_metric = list()
    # for example in list_example:
    #     prediction = predict_is_supporting_opt(
    #                             first_statement  = example.first_statement,
    #                             second_statement = example.second_statement)
    #     metric = _metric_is_supporting_consistency(None, prediction)
    #     list_metric.append(metric)
    # model.inspect_history(n = 10)
    # plot_histogram(list_metric)
    # print('=' * 80)
    # print('=' * 80)



# -----------------------------------------------------------------------------
def plot_histogram(scores):
    seaborn.set(style="whitegrid")
    matplotlib.pyplot.figure(figsize=(8, 6))
    seaborn.histplot(scores, kde = False, bins = 4)
    matplotlib.pyplot.title("Histogram of consistency metric values.")
    matplotlib.pyplot.xlabel("Metric value")
    matplotlib.pyplot.ylabel("Count")
    matplotlib.pyplot.xticks([25, 50, 75, 100])  # Set custom x-axis ticks
    matplotlib.pyplot.xlim(0, 100)
    matplotlib.pyplot.show()


# =============================================================================
class ModuleIsSupporting(dspy.Module):

    # -------------------------------------------------------------------------
    def __init__(self, num_samples, max_retries = 4):
        """
        Return a constructed predictor module.

        """

        super().__init__()

        self.max_retries           = max_retries
        self.predict_is_supporting = dspy.ChainOfThought(
                                                SignatureIsSupporting,
                                                n = num_samples)

    # -------------------------------------------------------------------------
    def forward(self, first_statement, second_statement):
        """
        Return the prediction.

        """

        prediction = self.predict_is_supporting(
                                    first_statement  = first_statement,
                                    second_statement = second_statement)

        list_completion = list(prediction.completions)
        set_allowed     = {'True', 'False'}
        is_valid        = all(completion.is_supporting in set_allowed
                                        for completion in list_completion)

        dspy.Suggest(result        = is_valid,
                     msg           = 'Output should be "True" or "False"',
                     target_module = self.predict_is_supporting)

        return dspy.Prediction(
                    first_statement  = first_statement,
                    second_statement = second_statement,
                    is_supporting    = prediction.is_supporting,
                    rationale        = prediction.rationale,
                    list_completion  = list_completion)


# =============================================================================
class SignatureIsSupporting(dspy.Signature):
    """
    Determine if the second statement supports the first statement in an argument.

    """

    first_statement  = dspy.InputField(
                                    desc = 'The first_statement may or '
                                           'may not be supported by the '
                                           'second_statement')

    second_statement = dspy.InputField(
                                    desc = 'The second_statement may or '
                                           'may not provide support for '
                                           'the first_statement')

    is_supporting    = dspy.OutputField(
                                    desc = '"True" if the second_statement '
                                           'supports the first_statment '
                                           'and "False" otherwise.')

    # The comment field makes GPT3.5 more consistently able
    # to output restricted values.
    #
    comment          = dspy.OutputField(
                                    desc = 'The reason behind the choice of '
                                           'is_supporting value.')

# -----------------------------------------------------------------------------
def _metric_is_supporting_consistency(example, pred, trace=None):
    """
    Return a metric indicating the consistency of the is_supporting field.

    The metric will be 100 if is_supporting is
    entirely consistent, and 0 if is_supporing
    is split 50/50 between true/false.

    """

    list_str    = list(item.is_supporting for item in pred.list_completion)
    set_allowed = {'True', 'False'}
    is_valid    = all(str_item in set_allowed for str_item in list_str)

    if not is_valid:

        metric = 0

    else:

        count_total = len(list_str)
        hist        = collections.Counter(list_str)
        count_bins  = len(hist)

        assert count_bins in {1, 2}  # Each string can only be True or False

        if count_bins == 1:
            ratio_mode_to_total = 1
        elif count_bins == 2:
            item_modal          = max(hist.items(), key = lambda it: it[1])
            bin_height_modal    = item_modal[1]
            ratio_mode_to_total = bin_height_modal / count_total  # range 0.5-1
        else:
            raise RuntimeError('Expecting only one or two bins.')

        assert ratio_mode_to_total <= 1
        assert ratio_mode_to_total >= 0.5

        metric = 100 * (2 * (ratio_mode_to_total - 0.5))

    metric_threshold = 80
    if trace:
        is_ok = metric >= metric_threshold
        return is_ok
    else:
        return metric


# -----------------------------------------------------------------------------
def _parse_boolean(str_bool: str):
    """
    Return boolean True if str_bool is equal to "True", boolean False otherwise.

    This performs a case insensitive comparison,
    so "TRUE", "True", "true" and other case
    variations of the word "True" will all return
    boolean True. Any other string will return
    boolean False.

    """

    is_true = str_bool.upper() == 'TRUE'
    return is_true


# -----------------------------------------------------------------------------
def _language_model(id_model):
    """
    Return the language model.

    """

    openai.organization = 'org-NHeev4fzi596aHqgtgqUTahT'

    return dspy.OpenAI(model      = id_model,
                       max_tokens = 350,
                       api_key    = key.load('APIKEY_OPENAI'))


LIST_STR_STATEMENT = ['Is it morally acceptable for wealthy countries to have access to the majority of the world’s resources, while poorer countries struggle to provide for their citizens?',
                      'No, it’s not morally acceptable. Ideally, resources should be distributed equitably among countries to promote equal growth and opportunities.',
                      'That’s an interesting perspective. Let’s delve deeper into the concept of ’equitable distribution’. Could you explain what equitable distribution of resources looks like to you? And do you think it’s feasible to achieve considering the diverse economic capabilities and needs of different nations?',
                      'Equitable distribution of resources means that each country gets a fair share based on its needs, population, and capacity. It doesn’t necessarily mean equal, but it considers the needs of each. Achieving this is challenging due to differences in economic structures, government systems, and power dynamics. However, effort towards it can be made through international cooperation and policies that promote sustainability and fair trade.',
                      'You bring up a very pertinent point about the need for international cooperation and equitable policies. However, as grounded in history, we’ve seen nations often act out of economic self-interest. How do we address this challenge and incentivize nations to cooperate effectively in resource distribution, disregarding their self-interests to a certain extent?',
                      'Incentivizing nations can be through creating global policies that reward sustainable and equitable practices, similar to carbon credits in environmental conservation. Educating citizens and promoting social responsibility can also create pressure on governments. Moreover, demonstrating that long-term survival and economic growth demand cooperative international relations and fair resource distribution could be persuasive.',
                      'That’s a thoughtful response. You mentioned the creation of global policies and reforms for achieving equitable practices. This leads us to consider a very crucial factor: the political stability and governance of individual nations. How do you think the effectiveness of these policies is affected by the varying stability and governance in different nations? Can you think of any instances where the political climate may complicate the successful implementation of such policies?',
                      'Certainly, political stability and governance can greatly impact the execution and effectiveness of global equity policies. Countries with unstable governance or those involved in conflicts might not prioritize these policies. Corruption could also affect the implementation. For example, development aid aimed at resource distribution might not reach its intended beneficiaries in a corrupt system. Additionally, some nationalistic governments might resist policies that seem to compromise their sovereignty or economic competitiveness. These complexities make the enforcement of such global policies a significant challenge.',
                      'Your points regarding the tumultuous nature of political stability and governance, and its impact on the implementation of global equity policies, are well stated. Shifting gears a bit, let’s look at the other side of the coin – the consequences of the current wealth and resource disparity. Could you elaborate on the ethical implications of this disparity, and how it might be contributing to issues such as global poverty and inequality?',
                      'Certainly, the profound wealth and resource disparities existing today have several ethical implications. It leads to unequal opportunities, allowing a small portion of the population to have access to vast resources, while a significant portion struggles to meet basic needs. This disparity propagates social and economic inequalities and perpetuates systems of poverty. Furthermore, it challenges the principles of fairness and justice, as it usually stems not from a lack of resources, but from an inequitable distribution. It also complicates the achievement of sustainable development and universal human rights.',
                      'You make a strong case about the ethical implications of wealth and resource disparities. However, you’ve made an assumption that the root problem is primarily inequitable distribution, not a lack of resources. How have you arrived at this conclusion, especially considering scenarios where the availability of resources itself might be limited? Could that not also contribute to the disparities we see?',
                      'I apologize if my previous statement was a bit broad. In fact, it’s a complex issue. Both the inequitable distribution and scarcity of resources contribute to wealth and resource disparities. In numerous cases, ample resources exist, but their distribution is skewed favoring a small section of the population. However, there are certainly scenarios where the limited availability of resources can exacerbate disparities, especially in regions that lack critical natural resources or when resources are exhausted due to overuse or poor management. Both issues are of significant concern.',
                      'You argue that resource disparities inherently perpetuate systems of poverty and socio-economic inequalities. This is a substantial claim. Could you provide some evidence or specific examples to support this theory? Also, it may strengthen your argument to consider if there might be any exceptions or counterexamples where this was not the case.',
                      'Indeed, consider the example of South Africa, one of the most unequal countries globally, where a small proportion of the population controls a substantial portion of wealth and resources, leaving the majority in poverty. Conversely, countries like Sweden and Denmark have very less resource disparity due to supportive social systems, and they exhibit lower poverty rates. However, it’s not a rule that resource disparity always leads to poverty. East Asian countries like Singapore and Hong Kong have high income inequality but low rates of poverty because their policies ensure that a minimum standard of living is maintained. They’ve achieved this through robust social security systems and investments in education and healthcare.',
                      'That’s a comprehensive assessment, connecting resource disparity to poverty and socio-economic inequalities through specific examples. Now, let’s pivot from this ethical perspective and start considering the pragmatic aspects of resource distribution. How do you think factors such as economies, governance, infrastructure, and human capital modify our understanding of equitable distribution and practical solutions?',
                      'Economies, governance, infrastructure, and human capital are critical components in addressing resource distribution. For instance, a strong economy can generate resources and wealth; however, without proper governance and policies, these may not be equitably distributed. Good governance is necessary to implement policies promoting fairness. Infrastructure plays a vital role too. For example, well-developed transport systems can ensure resources reach remote areas, while efficient internet connectivity can provide equal access to digital resources. Human capital, i.e., the skills and abilities of the population, is also important as it determines how efficiently resources are used. For example, a well-educated population is more likely to use resources optimally and contribute to generating more resources. All these aspects significantly affect how equitable distribution is achieved, and solutions should consider how these factors interplay in a particular context.',
                      'That’s a compelling synthesis of how these factors can impact resource distribution. However, different societies have varied contexts, demands, and cultural norms. Do you believe this model of resource distribution and the factors influencing it can be universally applied? Could there be instances where some of these factors are less important or not applicable at all?',
                      'Distinct societal factors indeed mean that it’s not a one-size-fits-all approach when it comes to resource distribution. Cultural norms, for instance, can influence perceptions of what is considered equitable. In some communities, assets might be traditionally controlled by a particular group, affecting distribution. Moreover, in technologically advanced societies, digital infrastructure holds major significance, while in less developed, agrarian societies, physical infrastructure may be paramount. Thus, while the factors of economies, governance, infrastructure, and human capital are universally relevant, the emphasis on each can vary based on the unique socio-economic and cultural context of a society. It’s essential to tailor resource distribution strategies to individual societal needs and characteristics for effectiveness.',
                      'That’s an insightful analysis. However, your evaluation seems to assume that economies, governance, infrastructure, and human capital always function optimally. Let’s ponder upon potential obstacles or imperfections within these systems. Can you think of situations where inefficiencies in these areas may obstruct the goal of equitable resource distribution?',
                      'Yes, inefficiencies can indeed obstruct equitable resource distribution. Economies: Economic recessions or mismanagement might limit available resources, making equitable distribution harder. Governance: Corruption or lack of transparency can lead to resource hoarding by a privileged few. Infrastructure: Inadequate infrastructure can prevent resources from reaching certain communities or regions. Human Capital: Low levels of education or skill may result in sub-optimal utilization of resources, affecting equity. Addressing these challenges requires systemic improvements and monitoring.']


# -----------------------------------------------------------------------------
def _generate_list_example():
    """
    Generate a dataset consisting of a list of odered pairs

    """

    list_example = []
    for ordered_pair in _gen_ordered_pairs(LIST_STR_STATEMENT):
        (first_statement, second_statement) = ordered_pair
        list_example.append(
            dspy.primitives.Example(
                first_statement  = first_statement,
                second_statement = second_statement).with_inputs(
                                                        'first_statement',
                                                        'second_statement'))
    return list_example

# -----------------------------------------------------------------------------
def _gen_ordered_pairs(iter_items):
    """
    Yield ordered pairs drawn from the specified iterable.

    """

    return itertools.combinations(iter_items, 2)
