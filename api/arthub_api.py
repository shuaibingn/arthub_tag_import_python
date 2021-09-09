from utils.http import post, get


def get_child_node_id_in_range(url, folder_id, header):
    body = {
        "parent_id": folder_id,
        "offset": 0,
        "count": -1,
        "filter": [],
        "order": {"meta": "order_weight", "type": "descend"},
        "is_recursive": False
    }
    resp = post(url, headers=header, json=body)
    return resp


def get_node_brief_by_id(url, ids: list, header: dict):
    body = {
        "ids": ids,
        "meta": ["id", "name", "name_pinyin", "parent_id", "node_type"]
    }
    resp = post(url, headers=header, json=body)
    return resp


def get_tag_id_by_asset_id(url, asset_id, header: dict):
    resp = get(f"{url}?asset_id={asset_id}", headers=header)
    return resp


def get_tag_detail_by_id(url, tag_ids: list, header: dict):
    body = {"ids": tag_ids}
    resp = post(url, headers=header, json=body)
    return resp


def delete_asset_tag(url, asset_id, tag_name: list, header: dict):
    body = {"asset_id": asset_id, "tag_name": tag_name}
    resp = post(url, headers=header, json=body)
    return resp


def add_asset_tag(url, asset_id, tag_name: list, header: dict):
    body = {"asset_id": asset_id, "tag_name": tag_name}
    resp = post(url, headers=header, json=body)
    return resp


# if __name__ == '__main__':
#     h = {"publictoken": "2012b"}
    # u1 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/get-child-node-id-in-range"
    # r1 = get_child_node_id_in_range(u1, h)
    # u2 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/get-node-brief-by-id"
    # get_node_brief_by_id(u2, r1.get("result").get("nodes"), h)
    # u3 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/get-tag-id-by-asset-id"
    # get_tag_id_by_asset_id(u3, 131353, h)
    # u4 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/get-tag-detail-by-id"
    # get_tag_detail_by_id(u4, [131356], h)
    # u5 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/delete-asset-tag"
    # delete_asset_tag(u5, 131353, ["test"], h)
    # u6 = "http://arthub-api.h3d.com.cn/h3d/data/openapi/v2/core/add-asset-tag"
    # add_asset_tag(u6, 131353, ["test"], h)
