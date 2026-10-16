import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service
# ================================================================ # CAP DO 1: Bo test co ban cho san (Moi chi dat ~35% Coverage)
# ================================================================ 
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang""" 
    def setUp(self):
        self.app = YummyApp() 
    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2} 
        self.assertEqual(self.app.calculate_order_total(cart), 100000)
    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1} 
        self.assertEqual(self.app.calculate_order_total(cart), 95000)
    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)
    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0} 
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)
# ================================================================ # CAP DO 2 (TIET 3): SINH VIEN TU TAY LAP TRINH TEST CASE DUOI DAY
# (Sau khi da hoan thanh Ban thiet ke test case viet tay tren giay)
# ================================================================
# Sinh vien tu viet class TestMediumLevel o day (4 test case cho apply_promo_code) # ...
class TestMediumLevel(unittest.TestCase):
    """Kiểm thử chức năng áp dụng mã khuyến mãi apply_promo_code"""

    def test_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(result, 90000.0)

    def test_promo_offline_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_special_os15_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(result, 80000.0)

    def test_promo_special_os14_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")
# Sinh vien tu viet class TestHardLevel o day (@patch cho get_nearby_restaurants) # ...
class TestHardLevel(unittest.TestCase):
    """Kiểm thử dịch vụ vị trí get_nearby_restaurants với Mocking GPS"""

    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_nearby_in_range(self, mock_get_location):
        mock_get_location.return_value = (10.0, 105.0)
        restaurants = self.app.get_nearby_restaurants()
        self.assertEqual(restaurants, ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"])

    @patch('yummy_app.gps_service.get_current_location')
    def test_nearby_out_of_range(self, mock_get_location):
        mock_get_location.return_value = (20.0, 110.0)
        restaurants = self.app.get_nearby_restaurants()
        self.assertEqual(restaurants, [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_nearby_gps_signal_lost(self, mock_get_location):
        mock_get_location.side_effect = gps_service.GPSSignalLostError
        result = self.app.get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")

if __name__ == '__main__':
    unittest.main()
