import json
import logging
from datetime import datetime

import pytest
import requests

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.FileHandler("api_test.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# 基本API配置
BASE_URL = "https://api-with-bugs.practicesoftwaretesting.com"
PRODUCTS_ENDPOINT = f"{BASE_URL}/products"

# 測試數據
TEST_PRODUCT = {"name": "Test Product", "description": "This is a test product", "price": 19.99, "category_id": 1, "brand_id": 1, "product_image_id": 1, "is_location_offer": 0, "is_rental": 0}

# 通用Header，包含JSON內容類型
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """設置和清理測試環境"""
    # 設置部分
    logger.info(f"開始測試，時間：{datetime.now()}")
    yield
    # 清理部分
    logger.info(f"結束測試，時間：{datetime.now()}")


@pytest.mark.get
@pytest.mark.basic
def test_get_all_products():
    """測試獲取所有產品功能"""
    logger.info("執行測試：獲取所有產品")
    response = requests.get(PRODUCTS_ENDPOINT)

    # 驗證狀態碼
    assert response.status_code == 200

    # 驗證響應是JSON格式
    data = response.json()

    # 驗證包含所有必要欄位
    assert "current_page" in data
    assert "data" in data
    assert "from" in data
    assert "last_page" in data
    assert "per_page" in data
    assert "to" in data
    assert "total" in data

    # 驗證data是陣列且不為空
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


@pytest.mark.get
@pytest.mark.pagination
def test_pagination():
    """測試分頁功能"""
    logger.info("執行測試：分頁功能")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?page=2")

    # 驗證狀態碼
    assert response.status_code == 200

    # 驗證是第二頁
    data = response.json()
    assert data["current_page"] == 2

    # 驗證data是陣列且不為空
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


@pytest.mark.get
@pytest.mark.filter
def test_price_range_filter():
    """測試價格範圍篩選功能"""
    logger.info("執行測試：價格範圍篩選")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?between=price%2C10%2C15")

    # 驗證狀態碼
    assert response.status_code == 200

    # 驗證所有產品價格在10-15範圍內
    data = response.json()
    for product in data["data"]:
        assert 10 <= float(product["price"]) <= 15


@pytest.mark.get
@pytest.mark.sort
def test_sort_by_name_desc():
    """測試按名稱降序排序功能"""
    logger.info("執行測試：按名稱降序排序")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?sort=name%2Cdesc")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 如果產品數據少於2個，無法驗證排序
    if len(data["data"]) < 2:
        pytest.skip("產品數量少於2，無法驗證排序")

    # 獲取所有產品名稱
    product_names = [product["name"] for product in data["data"]]

    # 複製並按降序排序
    sorted_names = sorted(product_names, reverse=True)

    # 比較原始順序與排序後順序
    assert product_names == sorted_names


@pytest.mark.get
@pytest.mark.sort
def test_sort_by_name_asc():
    """測試按名稱升序排序功能"""
    logger.info("執行測試：按名稱升序排序")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?sort=name%2Casc")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 如果產品數據少於2個，無法驗證排序
    if len(data["data"]) < 2:
        pytest.skip("產品數量少於2，無法驗證排序")

    # 獲取所有產品名稱
    product_names = [product["name"] for product in data["data"]]

    # 複製並按升序排序
    sorted_names = sorted(product_names)

    # 比較原始順序與排序後順序
    assert product_names == sorted_names


@pytest.mark.get
@pytest.mark.sort
def test_sort_by_price_desc():
    """測試按價格降序排序功能"""
    logger.info("執行測試：按價格降序排序")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?sort=price%2Cdesc")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 如果產品數據少於2個，無法驗證排序
    if len(data["data"]) < 2:
        pytest.skip("產品數量少於2，無法驗證排序")

    # 獲取所有產品價格
    product_prices = [float(product["price"]) for product in data["data"]]

    # 檢查是否按降序排序
    for i in range(len(product_prices) - 1):
        assert product_prices[i] >= product_prices[i + 1]


@pytest.mark.get
@pytest.mark.sort
def test_sort_by_price_asc():
    """測試按價格升序排序功能"""
    logger.info("執行測試：按價格升序排序")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?sort=price%2Casc")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 如果產品數據少於2個，無法驗證排序
    if len(data["data"]) < 2:
        pytest.skip("產品數量少於2，無法驗證排序")

    # 獲取所有產品價格
    product_prices = [float(product["price"]) for product in data["data"]]

    # 檢查是否按升序排序
    for i in range(len(product_prices) - 1):
        assert product_prices[i] <= product_prices[i + 1]


@pytest.mark.get
@pytest.mark.basic
def test_get_single_product():
    """測試獲取單個產品功能"""
    logger.info("執行測試：獲取單個產品")
    product_id = "1"  # 假設ID 1存在
    response = requests.get(f"{PRODUCTS_ENDPOINT}/{product_id}")

    # 驗證狀態碼
    assert response.status_code == 200

    # 驗證產品ID
    data = response.json()
    assert str(data["id"]) == product_id


@pytest.mark.get
@pytest.mark.combination
def test_combined_parameters():
    """測試參數組合使用功能"""
    logger.info("執行測試：參數組合使用")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?between=price%2C10%2C15&sort=name%2Casc")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 驗證價格範圍
    for product in data["data"]:
        assert 10 <= float(product["price"]) <= 15

    # 如果產品數據少於2個，無法驗證排序
    if len(data["data"]) < 2:
        pytest.skip("產品數量少於2，無法驗證排序")

    # 獲取所有產品名稱
    product_names = [product["name"] for product in data["data"]]

    # 複製並按升序排序
    sorted_names = sorted(product_names)

    # 比較原始順序與排序後順序
    assert product_names == sorted_names


@pytest.mark.post
@pytest.mark.exploratory
def test_post_without_id():
    """測試不帶ID的POST請求，探索行為"""
    logger.info("執行測試：不帶ID的POST請求")
    response = requests.post(PRODUCTS_ENDPOINT, headers=HEADERS, data=json.dumps(TEST_PRODUCT))

    # 記錄響應狀態碼和內容以便觀察
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    # 如果是創建操作，狀態碼應為201
    if response.status_code == 201:
        data = response.json()
        assert "id" in data

    # 統計驗證，允許非201狀態碼，但記錄下來
    assert response.status_code in [201, 400, 401, 403, 404, 405, 422, 500]


@pytest.mark.post
@pytest.mark.exploratory
def test_post_with_id():
    """測試帶ID的POST請求，探索行為"""
    logger.info("執行測試：帶ID的POST請求")
    product_id = "11"  # 假設ID 11存在
    response = requests.post(f"{PRODUCTS_ENDPOINT}/{product_id}",
                             headers=HEADERS,
                             data=json.dumps({
                                 "name": "Updated Product",
                                 "description": "This is an updated product",
                                 "price": 29.99,
                                 "category_id": 1,
                                 "brand_id": 1,
                                 "product_image_id": 1,
                                 "is_location_offer": 0,
                                 "is_rental": 0
                             }))

    # 記錄響應狀態碼和內容以便觀察
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    # 允許多種可能的狀態碼
    assert response.status_code in [200, 201, 204, 400, 401, 403, 404, 405, 422, 500]


@pytest.mark.post
@pytest.mark.error
def test_post_with_id_missing_required_fields():
    """測試帶ID的POST請求但缺少必填字段的情況"""
    logger.info("執行測試：帶ID的POST請求缺少必填字段")
    product_id = "11"  # 假設ID 11存在
    response = requests.post(f"{PRODUCTS_ENDPOINT}/{product_id}", headers=HEADERS, data=json.dumps({"name": "Incomplete Product"}))

    # 驗證狀態碼
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    assert response.status_code in [400, 422]

    # 驗證響應包含錯誤信息
    try:
        data = response.json()
        assert any(key in data for key in ["message", "error", "errors"])
    except:
        pytest.fail("回應不是有效的JSON或不包含錯誤信息")


@pytest.mark.post
@pytest.mark.error
def test_post_with_id_invalid_price():
    """測試帶ID的POST請求但使用無效價格的情況"""
    logger.info("執行測試：帶ID的POST請求使用無效價格")
    product_id = "11"  # 假設ID 11存在
    response = requests.post(f"{PRODUCTS_ENDPOINT}/{product_id}",
                             headers=HEADERS,
                             data=json.dumps({
                                 "name": "Negative Price Product",
                                 "description": "This product has a negative price",
                                 "price": -10.99,
                                 "category_id": 1,
                                 "brand_id": 1,
                                 "product_image_id": 1,
                                 "is_location_offer": 0,
                                 "is_rental": 0
                             }))

    # 驗證狀態碼
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    assert response.status_code in [400, 422]

    # 驗證響應包含錯誤信息
    try:
        data = response.json()
        assert any(key in data for key in ["message", "error", "errors"])
    except:
        pytest.fail("回應不是有效的JSON或不包含錯誤信息")


@pytest.mark.get
@pytest.mark.error
def test_nonexistent_product():
    """測試請求不存在的產品ID"""
    logger.info("執行測試：請求不存在的產品ID")
    response = requests.get(f"{PRODUCTS_ENDPOINT}/999999")

    # 驗證狀態碼
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    assert response.status_code == 404

    # 驗證響應包含錯誤信息
    try:
        data = response.json()
        assert any(key in data for key in ["message", "error"])
    except:
        pytest.fail("回應不是有效的JSON或不包含錯誤信息")


@pytest.mark.post
@pytest.mark.error
def test_post_nonexistent_product():
    """測試向不存在的產品ID發送POST請求"""
    logger.info("執行測試：向不存在的產品ID發送POST請求")
    response = requests.post(f"{PRODUCTS_ENDPOINT}/999999", headers=HEADERS, data=json.dumps(TEST_PRODUCT))

    # 驗證狀態碼
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    assert response.status_code == 404

    # 驗證響應包含錯誤信息
    try:
        data = response.json()
        assert any(key in data for key in ["message", "error"])
    except:
        pytest.fail("回應不是有效的JSON或不包含錯誤信息")


@pytest.mark.get
@pytest.mark.error
def test_between_with_nonexistent_field():
    """測試使用不存在的欄位進行between查詢"""
    logger.info("執行測試：使用不存在的欄位進行between查詢")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?between=ABCD1234%2C10%2C15")

    # 記錄響應
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    # 驗證API正確處理了請求（不一定是200，可能是錯誤碼）
    assert response.status_code in [200, 400, 404, 422, 500]


@pytest.mark.get
@pytest.mark.error
def test_sort_with_nonexistent_field():
    """測試使用不存在的欄位進行排序"""
    logger.info("執行測試：使用不存在的欄位進行排序")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?sort=ABCD1234%2Casc")

    # 記錄響應
    logger.info(f"Status code: {response.status_code}")
    try:
        logger.info(f"Response: {response.json()}")
    except:
        logger.info(f"Response text: {response.text}")

    # 驗證API正確處理了請求（不一定是200，可能是錯誤碼）
    assert response.status_code in [200, 400, 404, 422, 500]


@pytest.mark.get
@pytest.mark.filter
def test_specific_price():
    """測試查詢特定價格的產品"""
    logger.info("執行測試：查詢特定價格的產品")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?between=price%2C14.15%2C14.15")

    # 驗證狀態碼
    assert response.status_code == 200

    data = response.json()

    # 如果沒有找到符合條件的產品，測試通過
    if len(data["data"]) == 0:
        logger.info("沒有找到價格為14.15的產品")
        return

    # 驗證所有返回的產品價格等於14.15（允許微小誤差）
    for product in data["data"]:
        assert abs(float(product["price"]) - 14.15) < 0.001


@pytest.mark.get
@pytest.mark.filter
@pytest.mark.error
def test_negative_price_range():
    """測試使用負值價格範圍進行查詢"""
    logger.info("執行測試：使用負值價格範圍進行查詢")
    response = requests.get(f"{PRODUCTS_ENDPOINT}?between=price%2C-10%2C-5")

    # 記錄響應
    logger.info(f"Status code: {response.status_code}")
    try:
        data = response.json()
        logger.info(f"Response: {data}")

        if response.status_code == 200:
            if len(data["data"]) == 0:
                logger.info("沒有找到負價格範圍的產品")
            else:
                logger.info(f"找到 {len(data['data'])} 個產品")
    except:
        logger.info(f"Response text: {response.text}")

    # 驗證API正確處理了請求（不一定是200，可能是錯誤碼）
    assert response.status_code in [200, 400, 404, 422, 500]


if __name__ == "__main__":
    logger.info("直接執行測試腳本，將使用pytest運行所有測試")
    pytest.main(["-v"])
