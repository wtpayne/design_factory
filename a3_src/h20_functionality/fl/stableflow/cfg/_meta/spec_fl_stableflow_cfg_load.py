# -*- coding: utf-8 -*-
"""
Functional specification for the fl.stableflow.cfg.load module.

"""


import itertools

import pytest

import pl.stableflow.util


# =============================================================================
class SpecifyFromPath:
    """
    Spec for the fl.stableflow.cfg.from_path function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_a_python_dict(self, filepath_cfg_yaml):
        """
        fl.stableflow.cfg.from_path returns a dict.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        assert isinstance(fl.stableflow.cfg.load.from_path(filepath_cfg_yaml),
                          dict)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_yaml_file(self, dict_of_strings, filepath_cfg_yaml):
        """
        fl.stableflow.cfg.from_path can load configuration from a YAML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(filepath_cfg_yaml),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_json_file(self, dict_of_strings, filepath_cfg_json):
        """
        fl.stableflow.cfg.from_path can load configuration from a JSON file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(filepath_cfg_json),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_xml_file(self, dict_of_strings, filepath_cfg_xml):
        """
        fl.stableflow.cfg.from_path can load configuration from an XML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(filepath_cfg_xml),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_yaml_files(
                                    self, dict_of_strings, dirpath_cfg_yaml):
        """
        fl.stableflow.cfg.from_path can load configuration from a YAML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(dirpath_cfg_yaml),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_json_files(
                                    self, dict_of_strings, dirpath_cfg_json):
        """
        fl.stableflow.cfg.from_path can load configuration from a JSON file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(dirpath_cfg_json),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_xml_files(
                                    self, dict_of_strings, dirpath_cfg_xml):
        """
        fl.stableflow.cfg.from_path can load configuration from an XML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_path(dirpath_cfg_xml),
                    dict_of_strings)


# =============================================================================
class SpecifyFromFilePath:
    """
    Spec for the fl.stableflow.cfg.load.from_filepath function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_a_python_dict(self, filepath_cfg_yaml):
        """
        fl.stableflow.cfg.load.from_filepath returns a dict.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        assert isinstance(fl.stableflow.cfg.load.from_filepath(filepath_cfg_yaml),
                          dict)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_yaml_file(self, dict_of_strings, filepath_cfg_yaml):
        """
        fl.stableflow.cfg.load.from_filepath can load config. from a YAML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_filepath(filepath_cfg_yaml),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_json_file(self, dict_of_strings, filepath_cfg_json):
        """
        fl.stableflow.cfg.load.from_filepath can load config. from a JSON file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_filepath(filepath_cfg_json),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_single_xml_file(self, dict_of_strings, filepath_cfg_xml):
        """
        fl.stableflow.cfg.load.from_filepath can load config. from an XML file.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_filepath(filepath_cfg_xml),
                    dict_of_strings)


# =============================================================================
class SpecifyLoad:
    """
    Spec for the fl.stableflow.cfg.load function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_returns_a_python_dict(self, dirpath_cfg_yaml):
        """
        fl.stableflow.cfg.load returns a dict.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        assert isinstance(fl.stableflow.cfg.load.from_dirpath(dirpath_cfg_yaml),
                          dict)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_yaml_files(
                                    self, dict_of_strings, dirpath_cfg_yaml):
        """
        fl.stableflow.cfg.load loads a directory of YAML files.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_dirpath(dirpath_cfg_yaml),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_json_files(
                                    self, dict_of_strings, dirpath_cfg_json):
        """
        fl.stableflow.cfg.load loads a directory of JSON files.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_dirpath(dirpath_cfg_json),
                    dict_of_strings)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_loads_a_directory_of_xml_files(
                                    self, dict_of_strings, dirpath_cfg_xml):
        """
        fl.stableflow.cfg.load loads a directory of XML files.

        """

        import fl.stableflow.cfg.load  # pylint: disable=C0415

        check_match(fl.stableflow.cfg.load.from_dirpath(dirpath_cfg_xml),
                    dict_of_strings)


# ------------------------------------------------------------------------------
def check_match(loaded, true):
    """
    Yield leaf values taken pairwise from the two specified nested maps.

    """

    for pair in itertools.zip_longest(_iter_leaves(loaded),
                                      _iter_leaves(true)):

        (pv_loaded, pv_true) = pair

        (path_loaded, value_loaded) = pv_loaded
        (path_true, value_true) = pv_true

        assert path_loaded == path_true
        assert value_loaded == value_true


# ------------------------------------------------------------------------------
def _iter_leaves(data_structure):
    """
    Yield al the leaf values in the specified data_structure.

    """

    for pv_pair in pl.stableflow.util.gen_path_value_pairs_depth_first(
                                                            data_structure):
        (_, value) = pv_pair
        is_interior_node = isinstance(value, (dict, list))
        is_leaf = not is_interior_node
        if is_leaf:
            yield pv_pair
