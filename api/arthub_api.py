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
