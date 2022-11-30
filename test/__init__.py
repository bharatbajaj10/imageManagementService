# from unittest.mock import Mock
# import sys
# import types
#
# module_name = 'boto3'
# boto3 = types.ModuleType(module_name)
# sys.modules[module_name] = boto3
#
# boto3.resource = Mock(name=module_name + '.resource')
# mock_resource = Mock()
# mock_table = Mock()
# mock_table.query.return_value = []
# mock_table.put_item.return_value = None
# mock_table.put_item.side_effect = Exception
# mock_resource.Table.return_value = mock_table
# boto3.resource.return_value = mock_resource
