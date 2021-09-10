api_response_error = "接口错误, 错误码: {}"
not_find_child_node = "没有找到目录"
delete_tag_error = "删除旧标签失败"
add_tag_error = "添加标签失败"


class ArtHubException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
