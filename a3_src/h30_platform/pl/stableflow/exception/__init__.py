# -*- coding: utf-8 -*-
"""
Package of classes representing various stableflow control signals.

"""


# =============================================================================
class ControlSignal(Exception):
    """
    Base class for custom exceptions used for controlling stableflow.

    """


# =============================================================================
class ImmediateHalt(ControlSignal):
    """
    Thrown or returned to trigger immediate process shutdown.

    This signal is used to initiate an
    immediate shutdown of the current
    process.

    In contrast with 'GracefulHalt', the
    system will respond to this signal
    in a manner that prioritizes shutting
    down the current process over ensuring
    that the system as a whole has
    shutdown cleanly and gracefully.

    As a consequence, the remaining
    processes and machines may need to
    be shut down manually.

    """

    # -------------------------------------------------------------------------
    def __init__(self, return_code):
        """
        Return an instance of an ImmediateHalt ControlSignal object.

        """

        self.return_code = return_code
        super().__init__()


# =============================================================================
class GracefulHalt(ControlSignal):
    """
    Thrown or returned to trigger graceful system shutdown.

    This signal is used to initiate a
    clean, controlled and systematic
    shutdown of the entire system.

    The system will respond to this
    signal in a manner that prioritizes
    ensuring that the system as a whole
    has shutdown cleanly and gracefully.

    As a consequence, the initiating
    component may continue to be
    called until the system shutdown
    is complete.

    """

    # -------------------------------------------------------------------------
    def __init__(self, return_code):
        """
        Return an instance of a GracefulHalt ControlSignal object.

        """

        self.return_code = return_code
        super().__init__()


# =============================================================================
class NonRecoverableError(ControlSignal):
    """
    Thrown to trigger controlled shutdown in an unplanned erroneous condition.

    This signal is used to initiate a
    controlled shutdown of the entire
    system when in an exceptional and
    unplanned condition of operation is
    encountered.

    This sort of condition is often
    referred to as a 'FatalError' in
    other systems.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cause):
        """
        Return an instance of a NonRecoverableError ControlSignal object.

        """

        self.cause = cause
        super().__init__()


# =============================================================================
class ResetAndRetry(ControlSignal):
    """
    Thrown to trigger a reset-and-retry on the current process.

    This can be used for contolled recovery from
    an error or exception.

    This sort of condition is often referred to as
    a 'NonFatalError' in other systems.

    """

    pass


# =============================================================================
class ApplicationException(ControlSignal):
    """
    Thrown to report an application level exception on the current process.

    """

    pass
