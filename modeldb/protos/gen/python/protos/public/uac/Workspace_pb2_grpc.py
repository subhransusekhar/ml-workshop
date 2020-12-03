# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from ..uac import Workspace_pb2 as uac_dot_Workspace__pb2


class WorkspaceServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getWorkspaceById = channel.unary_unary(
        '/ai.verta.uac.WorkspaceService/getWorkspaceById',
        request_serializer=uac_dot_Workspace__pb2.GetWorkspaceById.SerializeToString,
        response_deserializer=uac_dot_Workspace__pb2.Workspace.FromString,
        )
    self.getWorkspaceByName = channel.unary_unary(
        '/ai.verta.uac.WorkspaceService/getWorkspaceByName',
        request_serializer=uac_dot_Workspace__pb2.GetWorkspaceByName.SerializeToString,
        response_deserializer=uac_dot_Workspace__pb2.Workspace.FromString,
        )
    self.getWorkspaceByLegacyId = channel.unary_unary(
        '/ai.verta.uac.WorkspaceService/getWorkspaceByLegacyId',
        request_serializer=uac_dot_Workspace__pb2.GetWorkspaceByLegacyId.SerializeToString,
        response_deserializer=uac_dot_Workspace__pb2.Workspace.FromString,
        )


class WorkspaceServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def getWorkspaceById(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getWorkspaceByName(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getWorkspaceByLegacyId(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WorkspaceServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getWorkspaceById': grpc.unary_unary_rpc_method_handler(
          servicer.getWorkspaceById,
          request_deserializer=uac_dot_Workspace__pb2.GetWorkspaceById.FromString,
          response_serializer=uac_dot_Workspace__pb2.Workspace.SerializeToString,
      ),
      'getWorkspaceByName': grpc.unary_unary_rpc_method_handler(
          servicer.getWorkspaceByName,
          request_deserializer=uac_dot_Workspace__pb2.GetWorkspaceByName.FromString,
          response_serializer=uac_dot_Workspace__pb2.Workspace.SerializeToString,
      ),
      'getWorkspaceByLegacyId': grpc.unary_unary_rpc_method_handler(
          servicer.getWorkspaceByLegacyId,
          request_deserializer=uac_dot_Workspace__pb2.GetWorkspaceByLegacyId.FromString,
          response_serializer=uac_dot_Workspace__pb2.Workspace.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai.verta.uac.WorkspaceService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
