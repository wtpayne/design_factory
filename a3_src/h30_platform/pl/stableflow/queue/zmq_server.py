# -*- coding: utf-8 -*-
"""
ZeroMQ inter host queue server.

"""


import zmq


# =============================================================================
class Queue:
    """
    ZeroMQ inter host queue server.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cfg, cfg_edge, id_host):
        """
        Return an instance of a Queue object.

        """
        self.owner     = cfg_edge['owner']
        self.direction = cfg_edge['dirn']

        port    = _port_number(cfg['host'][id_host], cfg_edge)
        address = 'tcp://*:{port}'.format(port = port)
        is_src  = id_host == cfg_edge['id_host_src']

        if is_src:
            socket_type = zmq.PUB
        else:
            socket_type = zmq.SUB  # pylint: disable=E1101

        self._context = zmq.Context()
        self._socket  = self._context.socket(socket_type)
        self._socket.bind(address)

    # -------------------------------------------------------------------------
    def blocking_read(self):
        """
        Return the next item from the FIFO queue, waiting if necessary.

        """
        return self._socket.recv_pyobj()

    # -------------------------------------------------------------------------
    def non_blocking_write(self, msg):
        """
        Write to the end of the FIFO queue, raising an exception if full.

        """
        self._socket.send_pyobj(item)

    # -------------------------------------------------------------------------
    def approx_size(self):
        """
        Return the approximate size of the queue.

        """
        return None


# -----------------------------------------------------------------------------
def _port_number(cfg_host, cfg_edge):
    """
    Return the port number for the specified edge.

    """
    port_range    = cfg_host['port_range'].split('-')
    port_lo       = int(port_range[0])
    port_hi       = int(port_range[1])
    port          = port_lo + cfg_edge['idx_edge']
    if port > port_hi:
        raise RuntimeError('Insufficient port numbers available for graph')
    return port
