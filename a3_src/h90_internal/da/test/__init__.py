# -*- coding: utf-8 -*-
"""
---

title:
    "Test utility package."

description:
    "This package provides utility functions to
    run tests using pytest."

id:
    "72e4004a-7f58-47c9-b989-7d9cee4e2387"

type:
    dt002_python_package

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""


# -----------------------------------------------------------------------------
def all():
    """
    """
    import da.env
    tup_id_env         = tuple(da.env.iter_id_env())
    list_retval        = list()
    tup_id_tier_ignore = ('h00_thirdparty',
                          'h10_resource',
                          'h80_research')
    tup_id_env_ignore  = ('e000_design_automation_core',
                          'e001_process_assistant')
    for id_tier in da.env.tup_control_tier():

        if id_tier in tup_id_tier_ignore:
            continue

        for id_env in tup_id_env:

            if id_env in tup_id_env_ignore:
                continue

            list_retval.append(run_pytest(
                    path         = da.env.path(
                                        process_area = 'a3_src',
                                        control_tier = id_tier,
                                        relpath      = '.'),
                    filepath_cfg = da.env.path(
                                        process_area = 'a3_src',
                                        control_tier = 'h90_internal',
                                        relpath      = 'da/test/pytest.ini'),
                    id_env       = id_env,
                    expr_mark    = id_env))


# -----------------------------------------------------------------------------
def run(iter_path     = None,
        control_tier  = None,
        relpath       = None,
        id_env        = None,
        verbose_level = None,
        rootdir       = None):
    """
    Run test.

    """
    import da.env
    if iter_path is None:
        iter_path = list()
    if isinstance(iter_path, tuple):
        iter_path = list(iter_path)

    if id_env is None:
        id_env = 'e000_design_automation_core'

    has_control_tier = (control_tier is not  None)
    has_relpath      = (relpath      is not  None)
    if has_control_tier and has_relpath:
        iter_path.append(da.env.path(process_area = 'a3_src',
                                     control_tier = control_tier,
                                     relpath      = relpath))

    return run_pytest(
            path          = iter_path,
            filepath_cfg  = da.env.path(process_area = 'a3_src',
                                        control_tier = 'h90_internal',
                                        relpath      = 'da/test/pytest.ini'),
            id_env        = id_env,
            verbose_level = verbose_level,
            rootdir       = rootdir)


# -----------------------------------------------------------------------------
def run_pytest(
        path,
        expr_substring     = None,  # -k               Match substring expr.
        expr_mark          = None,  # -m               Match mark expr.
        do_marker_show     = None,  # --markers        Show markers.
        do_onerror_exit    = None,  # -x               Exit on first failure.
        do_showfix         = None,  # --fixtures       Show avail. fixtures.
        do_showfix_pertest = None,  # --fixtures-per-test
        do_onerror_debug   = None,  # --pdb            Debug on error.
        custom_debugger    = None,  # --pdbcls         Custom debugger.
        do_trace           = None,  # --trace          Trace debugging always.
        capture_method     = None,  # --capture        Per test capture method.
        do_xfail_run       = None,  # --runxfail       Report xfail tests also.
        do_lastfail_only   = None,  # --last-failed    Rerun failures only.
        do_lastfail_first  = None,  # --failed-first   Run failures first.
        do_newtest_first   = None,  # --new-first      Run new tests first.
        do_cache_show      = None,  # --cache-show     Show cache, do not test.
        do_cache_clear     = None,  # --cache-clear    Clear cache at start.
        lastfail_nofail    = None,  # --lfnf           What to run w/no fails.
        do_stepwise        = None,  # --stepwise       Continue from last fail.
        do_stepwise_skip   = None,  # --stepwise-skip  Stop on 2nd fail.
        show_duration      = None,  # --durations      Show n slowest.
        show_duration_min  = None,  # --durations-min  Min duration n slowest.
        verbose_inc        = None,  # --verbose        Increase verbosity.
        do_header_disable  = None,  # --no-header      Disable header display.
        do_summary_disable = None,  # --no-summary     Disable summary display.
        verbose_dec        = None,  # --quiet          Decrease verbosity.
        verbose_level      = None,  # --verbosity      Set verbosity.
        extra_info         = None,  # -r               Show extra summary info.
        do_warning_disable = None,  # --disable-warnings
        do_locals_show     = None,  # --showlocals     Show locals in trace.
        style_traceback    = None,  # --tb-style       Set traceback style.
        capture_display    = None,  # --show-capture   Set capture display.
        do_trace_full      = None,  # --full-trace     Show full trace.
        do_color           = None,  # --color          Show color.
        do_code_highlight  = None,  # --code-highlight Highlight code.
        pastebin           = None,  # --pastebin       Send to pastebin.
        junit_xml          = None,  # --junit-xml      Create JUnit report.
        junit_prefix       = None,  # --junit-prefix   Prepend prefix in JUnit.
        warnings           = None,  # -W               Set warmings.
        maxfail            = None,  # --maxfail        Exit after n failures.
        do_config_strict   = None,  # --strict-config  Fail on config warnings.
        do_markers_strict  = None,  # --strict-markers Fail on unknown markers.
        filepath_cfg       = None,  # -c               Load configuration file.
        do_continue_colerr = None,  # --continue-on-collection-errors
        rootdir            = None,  # --rootdir        Define test root dir.
        do_collect_only    = None,  # --collect-only   Collect, do not run.
        do_pyargs          = None,  # --pyargs         Args as python pkg.
        path_ignore        = None,  # --ignore         Ignore path.
        glob_ignore        = None,  # --ignore-glob    Ignore path glob.
        deselect           = None,  # --deselect       Deselect item.
        path_confcut       = None,  # --confcutdir     Only load conftest.py.
        do_no_conftest     = None,  # --noconftest     Don't load conftest.py.
        do_keep_dups       = None,  # --keep-duplicates
        do_collect_venv    = None,  # --collect-in-virtualenv
        import_mode        = None,  # --import-mode    Test import mode.
        do_doctest_modules = None,  # --doctest-modules  Run module doctests.
        doctest_report     = None,  # --doctest-report Doctest output format.
        doctest_glob       = None,  # --doctest-glob   Doctest file match.
        doctest_ignore     = None,  # --doctest-ignore-import-errors
        do_doctest_cont    = None,  # --doctest-continue-on-failure
        dirpath_tmp_base   = None,  # --basetemp       Base temp directory.
        do_display_version = None,  # --version        Show pytest version.
        do_display_help    = None,  # --help           Show pytest help.
        plugin             = None,  # -p               Select plugin.
        do_config_trace    = None,  # --trace-config   Trace conftest.py
        filepath_debug     = None,  # --debug          Logfile for debug info.
        ini_override       = None,  # --override-ini   Override .ini option.
        assert_mode        = None,  # --assert         Control assertion tools.
        do_setup_only      = None,  # --setup-only     Only setup fixtures.
        do_setup_show      = None,  # --setup-show     Show fixture setup.
        do_setup_plan      = None,  # --setup-plan     Show test plan.
        log_level          = None,  # --log-level      Set log level.
        log_fmt            = None,  # --log-format     Set log format.
        log_date_fmt       = None,  # --log-date-format
        log_cli_level      = None,  # --log-cli-level  Set log level.
        log_cli_fmt        = None,  # --log-cli-format Set log format.
        log_cli_date_fmt   = None,  # --log-cli-date-format
        log_file           = None,  # --log-file       Path to lof file.
        log_file_level     = None,  # --log-file-level Set file log level.
        log_file_fmt       = None,  # --log-file-format
        log_file_date_fmt  = None,  # --log-file-date-format
        log_auto_indent    = None,  # --log-auto-indent
        log_disable        = None,  # --log-disable    Disable a logger.
        id_env             = 'e000_design_automation_core',
        do_display_cmd     = False):
    """
    usage: pytest [options] [file_or_dir] [file_or_dir] [...]

    positional arguments:
      file_or_dir

    general:

      -k EXPRESSION                 Only run tests which match the given
                                    substring expression. An expression is a
                                    Python evaluatable expression where all
                                    names are substring-matched against test
                                    names and their parent classes. Example:
                                    -k 'test_method or test_other' matches all
                                    test functions and classes whose name
                                    contains 'test_method' or 'test_other',
                                    while -k 'not test_method' matches those
                                    that don't contain 'test_method' in their
                                    names. -k 'not test_method and not
                                    test_other' will eliminate the matches.
                                    Additionally keywords are matched to
                                    classes and functions containing extra
                                    names in their 'extra_keyword_matches'
                                    set, as well as functions which have names
                                    assigned directly to them. The matching is
                                    case-insensitive.

      -m MARKEXPR                   Only run tests matching given mark
                                    expression. For example: -m 'mark1 and not
                                    mark2'.

      --markers                     show markers (builtin, plugin and per-
                                    project ones).

      -x, --exitfirst               Exit instantly on first error or failed
                                    test

      --fixtures, --funcargs
                                    Show available fixtures, sorted by plugin
                                    appearance (fixtures with leading '_' are
                                    only shown with '-v')

      --fixtures-per-test           Show fixtures per test

      --pdb                         Start the interactive Python debugger on
                                    errors or KeyboardInterrupt

      --pdbcls=modulename:classname Specify a custom interactive Python
                                    debugger for use with --pdb.For example: -
                                    -pdbcls=IPython.terminal.debugger:Terminal
                                    Pdb

      --trace                       Immediately break when running each test

      --capture=method              Per-test capturing method: one of
                                    fd|sys|no|tee-sys

      -s                            Shortcut for --capture=no

      --runxfail                    Report the results of xfail tests as if
                                    they were not marked

      --lf, --last-failed           Rerun only the tests that failed at the
                                    last run (or all if none failed)

      --ff, --failed-first          Run all tests, but run the last failures
                                    first. This may re-order tests and thus
                                    lead to repeated fixture setup/teardown.

      --nf, --new-first             Run tests from new files first, then the
                                    rest of the tests sorted by file mtime

      --cache-show=[CACHESHOW]      Show cache contents, don't perform
                                    collection or tests. Optional argument:
                                    glob (default: '*').

      --cache-clear                 Remove all cache contents at start of test
                                    run

      --lfnf={all,none}, --last-failed-no-failures={all,none}
                                    Which tests to run with no previously
                                    (known) failures

      --sw, --stepwise              Exit on test failure and continue from
                                    last failing test next time

      --sw-skip, --stepwise-skip    Ignore the first failing test but stop on
                                    the next failing test. Implicitly enables
                                    --stepwise.

    Reporting:

      --durations=N                 Show N slowest setup/test durations (N=0
                                    for all)

      --durations-min=N             Minimal duration in seconds for inclusion
                                    in slowest list. Default: 0.005.

      -v, --verbose                 Increase verbosity

      --no-header                   Disable header

      --no-summary                  Disable summary

      -q, --quiet                   Decrease verbosity

      --verbosity=VERBOSE           Set verbosity. Default: 0.

      -r chars                      Show extra test summary info as specified
                                    by chars: (f)ailed, (E)rror, (s)kipped,
                                    (x)failed, (X)passed, (p)assed, (P)assed
                                    with output, (a)ll except passed (p/P), or
                                    (A)ll. (w)arnings are enabled by default
                                    (see --disable-warnings), 'N' can be used
                                    to reset the list. (default: 'fE').

      --disable-warnings, --disable-pytest-warnings
                                    Disable warnings summary

      -l, --showlocals              Show locals in tracebacks (disabled by
                                    default)

      --no-showlocals               Hide locals in tracebacks (negate
                                    --showlocals passed through addopts)

      --tb=style                    Traceback print mode
                                    (auto/long/short/line/native/no)

      --show-capture={no,stdout,stderr,log,all}
                                    Controls how captured stdout/stderr/log is
                                    shown on failed tests. Default: all.

      --full-trace                  Don't cut any tracebacks (default is to
                                    cut)

      --color=color                 Color terminal output (yes/no/auto)

      --code-highlight={yes,no}
                                    Whether code should be highlighted (only
                                    if --color is also enabled). Default: yes.

      --pastebin=mode               Send failed|all info to bpaste.net
                                    pastebin service

      --junit-xml=path              Create junit-xml style report file at
                                    given path

      --junit-prefix=str            Prepend prefix to classnames in junit-xml
                                    output

    pytest-warnings:

      -W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS
                                    Set which warnings to report, see -W
                                    option of Python itself

      --maxfail=num                 Exit after first num failures or errors

      --strict-config               Any warnings encountered while parsing the
                                    `pytest` section of the configuration file
                                    raise errors

      --strict-markers              Markers not registered in the `markers`
                                    section of the configuration file raise
                                    errors

      --strict                      (Deprecated) alias to --strict-markers

      -c file                       Load configuration from `file` instead of
                                    trying to locate one of the implicit
                                    configuration files

      --continue-on-collection-errors
                                    Force test execution even if collection
                                    errors occur

      --rootdir=ROOTDIR             Define root directory for tests. Can be
                                    relative path: 'root_dir', './root_dir',
                                    'root_dir/another_dir/'; absolute path:
                                    '/home/user/root_dir'; path with
                                    variables: '$HOME/root_dir'.

    collection:

      --collect-only, --co          Only collect tests, don't execute them

      --pyargs                      Try to interpret all arguments as Python
                                    packages

      --ignore=path                 Ignore path during collection (multi-
                                    allowed)

      --ignore-glob=path            Ignore path pattern during collection
                                    (multi-allowed)

      --deselect=nodeid_prefix      Deselect item (via node id prefix) during
                                    collection (multi-allowed)

      --confcutdir=dir              Only load conftest.py's relative to
                                    specified dir

      --noconftest                  Don't load any conftest.py files

      --keep-duplicates             Keep duplicate tests

      --collect-in-virtualenv       Don't ignore tests in a local virtualenv
                                    directory

      --import-mode={prepend,append,importlib}
                                    Prepend/append to sys.path when importing
                                    test modules and conftest files. Default:
                                    prepend.

      --doctest-modules             Run doctests in all .py modules

      --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                                    Choose another output format for diffs on
                                    doctest failure

      --doctest-glob=pat            Doctests file matching pattern, default:
                                    test*.txt

      --doctest-ignore-import-errors  Ignore doctest ImportErrors

      --doctest-continue-on-failure For a given doctest, continue to run after
                                    the first failure

    test session debugging and configuration:

      --basetemp=dir                Base temporary directory for this test
                                    run. (Warning: this directory is removed
                                    if it exists.)

      -V, --version                 Display pytest version and information
                                    about plugins. When given twice, also
                                    display information about plugins.

      -h, --help                    Show help message and configuration info

      -p name                       Early-load given plugin module name or
                                    entry point (multi-allowed). To avoid
                                    loading of plugins, use the `no:` prefix,
                                    e.g. `no:doctest`.

      --trace-config                Trace considerations of conftest.py files

      --debug=[DEBUG_FILE_NAME]     Store internal tracing debug information
                                    in this log file. This file is opened with
                                    'w' and truncated as a result, care
                                    advised. Default: pytestdebug.log.

      -o OVERRIDE_INI, --override-ini=OVERRIDE_INI
                                    Override ini option with "option=value"
                                    style, e.g. `-o xfail_strict=True -o
                                    cache_dir=cache`.

      --assert=MODE                 Control assertion debugging tools.
                                    'plain' performs no assertion debugging.
                                    'rewrite' (the default) rewrites assert
                                    statements in test modules on import to
                                    provide assert expression information.

      --setup-only                  Only setup fixtures, do not execute tests

      --setup-show                  Show setup of fixtures while executing
                                    tests

      --setup-plan                  Show what fixtures and tests would be
                                    executed but don't execute anything

    logging:

      --log-level=LEVEL                             Level of messages to
                                                    catch/display. Not set by
                                                    default, so it depends on
                                                    the root/parent log
                                                    handler's effective level,
                                                    where it is "WARNING" by
                                                    default.

      --log-format=LOG_FORMAT                       Log format used by the
                                                    logging module.

      --log-date-format=LOG_DATE_FORMAT             Log date format used by the
                                                    logging module.

      --log-cli-level=LOG_CLI_LEVEL CLI             logging level.

      --log-cli-format=LOG_CLI_FORMAT               Log format used by the
                                                    logging module.

      --log-cli-date-format=LOG_CLI_DATE_FORMAT     Log date format used by the
                                                    logging module.

      --log-file=LOG_FILE                           Path to a file when logging
                                                    will be written to.

      --log-file-level=LOG_FILE_LEVEL               Log file logging level.

      --log-file-format=LOG_FILE_FORMAT             Log format used by the
                                                    logging module.

      --log-file-date-format=LOG_FILE_DATE_FORMAT   Log date format used by the
                                                    logging module.

      --log-auto-indent=LOG_AUTO_INDENT             Auto-indent multiline
                                                    messages passed to the
                                                    logging module. Accepts
                                                    true|on, false|off or an
                                                    integer.

      --log-disable=LOGGER_DISABLE                  Disable a logger by name.
                                                    Can be passed multipe times.

    """

    # Set custom defaults.
    #
    import da.env
    if rootdir is None:
        rootdir = da.env.rootpath()

    # Append all provided options and
    # option-arguments together into
    # a list (list_opts), and then
    # concatenate the whole thing into
    # a single space delimited string.
    #
    list_opts = list()
    NONETYPE  = type(None)

    # -------------------------------------------------------------------------
    def flag(option, option_argument):
        """
        Add a boolean flag to the list of options.

        """
        assert isinstance(option_argument, (NONETYPE, bool))

        if option_argument is True:
            list_opts.append(option)

    # -------------------------------------------------------------------------
    def opt(option, option_argument):
        """
        Add an option to the list.

        """
        assert isinstance(option_argument, (NONETYPE, int, str))

        if option_argument is None:
            return
        if isinstance(option_argument, int):
            option_argument = str(option_argument)

        if option.startswith('--') and option.endswith('='):
            delimiter = ''
        else:
            delimiter = ' '

        list_opts.append(delimiter.join((option, option_argument)))

    # -------------------------------------------------------------------------
    def multi(option, option_argument):
        """
        Add an option to the list. (multi-allowed).

        """
        assert isinstance(option_argument, (NONETYPE, int, str, tuple, list))

        if option_argument is None:
            return

        if isinstance(option_argument, (tuple, list)):
            for item in option_argument:
                opt(option, item)
        else:
            opt(option, option_argument)

    # Define mapping from option to handling function
    #
    tup_tup_opthandler = (
        (opt,   expr_substring,     '-k'                                     ),
        (opt,   expr_mark,          '-m'                                     ),
        (flag,  do_marker_show,     '--markers'                              ),
        (flag,  do_onerror_exit,    '--exitfirst'                            ),
        (flag,  do_showfix,         '--fixtures'                             ),
        (flag,  do_showfix_pertest, '--fixtures-per-test'                    ),
        (flag,  do_onerror_debug,   '--pdb'                                  ),
        (opt,   custom_debugger,    '--pdbcls='                              ),
        (flag,  do_trace,           '--trace'                                ),
        (opt,   capture_method,     '--capture='                             ),
        (flag,  do_xfail_run,       '--runxfail'                             ),
        (flag,  do_lastfail_only,   '--last-failed'                          ),
        (flag,  do_lastfail_first,  '--failed-first'                         ),
        (flag,  do_newtest_first,   '--new-first'                            ),
        (opt,   do_cache_show,      '--cache-show='                          ),
        (flag,  do_cache_clear,     '--cache-clear'                          ),
        (opt,   lastfail_nofail,    '--last-failed-no-failures='             ),
        (flag,  do_stepwise,        '--stepwise'                             ),
        (flag,  do_stepwise_skip,   '--stepwise-skip'                        ),
        (opt,   show_duration,      '--durations='                           ),
        (opt,   show_duration_min,  '--durations-min='                       ),
        (flag,  verbose_inc,        '--verbose'                              ),
        (flag,  do_header_disable,  '--no-header'                            ),
        (flag,  do_summary_disable, '--no-summary'                           ),
        (flag,  verbose_dec,        '--quiet'                                ),
        (opt,   verbose_level,      '--verbosity='                           ),
        (opt,   extra_info,         '-r'                                     ),
        (flag,  do_warning_disable, '--disable-pytest-warnings'              ),
        (flag,  do_locals_show,     '--showlocals'                           ),
        (opt,   style_traceback,    '--tb='                                  ),
        (opt,   capture_display,    '--show-capture='                        ),
        (flag,  do_trace_full,      '--full-trace'                           ),
        (opt,   do_color,           '--color='                               ),
        (opt,   do_code_highlight,  '--code-highlight='                      ),
        (opt,   pastebin,           '--pastebin='                            ),
        (opt,   junit_xml,          '--junit-xml='                           ),
        (opt,   junit_prefix,       '--junit-prefix='                        ),
        (opt,   warnings,           '--pythonwarnings='                      ),
        (opt,   maxfail,            '--maxfail='                             ),
        (flag,  do_config_strict,   '--strict-config'                        ),
        (flag,  do_markers_strict,  '--strict-markers'                       ),
        (opt,   filepath_cfg,       '-c'                                     ),
        (flag,  do_continue_colerr, '--continue-on-collection-errors'        ),
        (opt,   rootdir,            '--rootdir='                             ),
        (flag,  do_collect_only,    '--collect-only'                         ),
        (flag,  do_pyargs,          '--pyargs'                               ),
        (multi, path_ignore,        '--ignore='                              ),
        (multi, glob_ignore,        '--ignore-glob='                         ),
        (multi, deselect,           '--deselect='                            ),
        (opt,   path_confcut,       '--confcutdir='                          ),
        (flag,  do_no_conftest,     '--noconftest'                           ),
        (flag,  do_keep_dups,       '--keep-duplicates'                      ),
        (flag,  do_collect_venv,    '--collect-in-virtualenv'                ),
        (opt,   import_mode,        '--import-mode='                         ),
        (flag,  do_doctest_modules, '--doctest-modules'                      ),
        (opt,   doctest_report,     '--doctest-report='                      ),
        (opt,   doctest_glob,       '--doctest-glob='                        ),
        (flag,  doctest_ignore,     '--doctest-ignore-import-errors'         ),
        (flag,  do_doctest_cont,    '--doctest-continue-on-failure'          ),
        (opt,   dirpath_tmp_base,   '--basetemp='                            ),
        (flag,  do_display_version, '--version'                              ),
        (flag,  do_display_help,    '--help'                                 ),
        (multi, plugin,             '-p'                                     ),
        (flag,  do_config_trace,    '--trace-config'                         ),
        (opt,   filepath_debug,     '--debug='                               ),
        (opt,   ini_override,       '--override-ini='                        ),
        (opt,   assert_mode,        '--assert='                              ),
        (flag,  do_setup_only,      '--setup-only'                           ),
        (flag,  do_setup_show,      '--setup-show'                           ),
        (flag,  do_setup_plan,      '--setup-plan'                           ),
        (opt,   log_level,          '--log-level='                           ),
        (opt,   log_fmt,            '--log-format='                          ),
        (opt,   log_date_fmt,       '--log-date-format='                     ),
        (opt,   log_cli_level,      '--log-cli-level='                       ),
        (opt,   log_cli_fmt,        '--log-cli-format='                      ),
        (opt,   log_cli_date_fmt,   '--log-cli-date-format='                 ),
        (opt,   log_file,           '--log-file='                            ),
        (opt,   log_file_level,     '--log-file-level='                      ),
        (opt,   log_file_fmt,       '--log-file-format='                     ),
        (opt,   log_file_date_fmt,  '--log-file-date-format='                ),
        (opt,   log_auto_indent,    '--log-auto-indent='                     ),
        (opt,   log_disable,        '--log-disable='                         ))

    for (closure_append, option_argument, option) in tup_tup_opthandler:
        closure_append(option, option_argument)

    if do_display_cmd:
        str_option_delimiter = ' \\\n   '  # Newlines to make it readable.
    else:
        str_option_delimiter = ' '

    str_opts = str_option_delimiter.join(list_opts)

    # Concatenate all provided paths
    # together into a space delimited
    # string.
    #
    if isinstance(path, str):
        path = [path]
    assert isinstance(path, (list, tuple))
    str_path = str_option_delimiter.join(path)

    str_command = 'pytest{delim}{args}{delim}{path}'.format(
                                                args  = str_opts,
                                                path  = str_path,
                                                delim = str_option_delimiter)

    if do_display_cmd:
        print(str_command)

    import da.env
    return da.env.run.shell_command(str_command, id_env = id_env)
