# -*- coding: utf-8 -*-
"""
Functional specification for fl.load.file

"""


import sys
import os.path

import pytest


# -----------------------------------------------------------------------------
def _get_rootpath_testdata():
    """
    Return the fully qualified path to the test data directory.

    """

    relfilepath_self  = __file__ if __file__ else sys.argv[0]
    filepath_self     = os.path.realpath(relfilepath_self)
    dirpath_self      = os.path.dirname(filepath_self)
    dirname_testdata  = 'testdata'
    rootpath_testdata = os.path.join(dirpath_self, dirname_testdata)

    return rootpath_testdata


# -----------------------------------------------------------------------------
def _get_map_dirpath_testdata():
    """
    Return a mapping of test data directory paths.

    """

    rootpath_testdata    = _get_rootpath_testdata()

    map_dirpath_testdata = {
        'zero_files':  os.path.join(rootpath_testdata, '00_zero_files'),
        'one_file':    os.path.join(rootpath_testdata, '01_one_file'),
        'two_files':   os.path.join(rootpath_testdata, '02_two_files'),
        'three_files': os.path.join(rootpath_testdata, '03_three_files'),
        'four_files':  os.path.join(rootpath_testdata, '04_four_files')
    }

    return map_dirpath_testdata


# =============================================================================
class SpecifyFlLoadFile:
    """
    Spec for the fl.load.file module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_load_file(self):
        """
        fl.load.file can be imported.

        """

        import fl.load.file


# =============================================================================
class SpecifyFlLoadFile_FilteredFilepathGenerator:
    """
    Spec for the fl.load.file._filtered_filepath_generator function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_the_expected_number_of_files(self):
        """
        fl.load.file._filtered_filepath_generator yields the correct file count.

        """

        import fl.load.file

        map_dirpath   = _get_map_dirpath_testdata()
        regex_tesfile = r'^.*\.testfile$'

        assert len(list(fl.load.file._filtered_filepath_generator(
                                    dirpath_root  = map_dirpath['zero_files'],
                                    iter_pathincl = (regex_tesfile,)))) == 0

        assert len(list(fl.load.file._filtered_filepath_generator(
                                    dirpath_root  = map_dirpath['one_file'],
                                    iter_pathincl = (regex_tesfile,)))) == 1

        assert len(list(fl.load.file._filtered_filepath_generator(
                                    dirpath_root  = map_dirpath['two_files'],
                                    iter_pathincl = (regex_tesfile,)))) == 2

        assert len(list(fl.load.file._filtered_filepath_generator(
                                    dirpath_root  = map_dirpath['three_files'],
                                    iter_pathincl = (regex_tesfile,)))) == 3

        assert len(list(fl.load.file._filtered_filepath_generator(
                                    dirpath_root  = map_dirpath['four_files'],
                                    iter_pathincl = (regex_tesfile,)))) == 4


# =============================================================================
class SpecifyFlLoadFile_GenerateFilepathAllOnce:
    """
    Spec for the fl.load.file._generate_filepath_all_once function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_the_expected_number_of_files(self):
        """
        fl.load.file._generate_filepath_all_once yields the correct file count.

        """

        import fl.load.file

        map_dirpath   = _get_map_dirpath_testdata()
        regex_tesfile = r'^.*\.testfile$'

        assert len(list(fl.load.file._generate_filepath_all_once(
                            iter_dirpath_root = (map_dirpath['zero_files'],),
                            iter_pathincl     = (regex_tesfile,)))) == 0

        assert len(list(fl.load.file._generate_filepath_all_once(
                            iter_dirpath_root = (map_dirpath['one_file'],),
                            iter_pathincl     = (regex_tesfile,)))) == 1

        assert len(list(fl.load.file._generate_filepath_all_once(
                            iter_dirpath_root = (map_dirpath['two_files'],),
                            iter_pathincl     = (regex_tesfile,)))) == 2

        assert len(list(fl.load.file._generate_filepath_all_once(
                            iter_dirpath_root = (map_dirpath['three_files'],),
                            iter_pathincl     = (regex_tesfile,)))) == 3

        assert len(list(fl.load.file._generate_filepath_all_once(
                            iter_dirpath_root = (map_dirpath['four_files'],),
                            iter_pathincl     = (regex_tesfile,)))) == 4



# =============================================================================
class SpecifyFlLoadFile_GenerateFilepathAll:
    """
    Spec for the fl.load.file._generate_filepath_all function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_the_expected_number_of_files(self):
        """
        fl.load.file._generate_filepath_all yields the correct file count.

        """

        import fl.load.file

        map_dirpath   = _get_map_dirpath_testdata()
        regex_tesfile = r'^.*\.testfile$'

        generate_two = fl.load.file._generate_filepath_all(
                            do_output_all     = True,
                            do_repeat_all     = False,
                            iter_dirpath_root = (map_dirpath['two_files'],),
                            iter_pathincl     = (regex_tesfile,))

        list_filepath = list()
        for idx in range(4):
            list_filepath.append(next(generate_two))

        assert list_filepath[0] is not None
        assert list_filepath[1] is not None
        assert list_filepath[2] is None
        assert list_filepath[3] is None

        generate_repeat = fl.load.file._generate_filepath_all(
                            do_output_all     = True,
                            do_repeat_all     = True,
                            iter_dirpath_root = (map_dirpath['two_files'],),
                            iter_pathincl     = (regex_tesfile,))

        list_filepath = list()
        for idx in range(4):
            list_filepath.append(next(generate_repeat))

        assert list_filepath[0] is not None
        assert list_filepath[1] is not None
        assert list_filepath[2] is not None
        assert list_filepath[3] is not None


# =============================================================================
class SpecifyFlLoadFile_GenListFilepath:
    """
    Spec for the fl.load.file._gen_list_filepath function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_the_expected_number_of_files(self):
        """
        fl.load.file._generate_filepath_all yields the correct file count.

        """

        import fl.load.file

        map_dirpath   = _get_map_dirpath_testdata()
        regex_tesfile = r'^.*\.testfile$'

        generate_two  = fl.load.file._gen_list_filepath(
                            iter_dirpath_root  = (map_dirpath['three_files'],),
                            iter_pathincl      = (regex_tesfile,),
                            size_batch         = 2,
                            do_output_all      = True,
                            do_repeat_all      = False,
                            do_output_modified = False)

        list_filepath = next(generate_two)
        assert len(list_filepath) == 2

        list_filepath = next(generate_two)
        assert len(list_filepath) == 1

        list_filepath = next(generate_two)
        assert len(list_filepath) == 0

