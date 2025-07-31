import unittest
from unittest.mock import patch
from ping2wechat import send_alert

class TestAlerts(unittest.TestCase):
    @patch('ping2wechat.requests.post')
    def test_send_alert_success(self, mock_post):
        """
        测试 send_alert 函数的成功请求
        """
        # 模拟 requests.post 返回 200 状态码
        mock_post.return_value.status_code = 200

        # 调用 send_alert 函数
        result = send_alert('test_hostname', '127.0.0.1', 'Test alert message')

        # 验证是否调用了 requests.post
        mock_post.assert_called_once()

        # 验证返回值为 True
        self.assertTrue(result)

    @patch('ping2wechat.requests.post')
    def test_send_alert_failure(self, mock_post):
        """
        测试 send_alert 函数的失败请求
        """
        # 模拟 requests.post 返回非 200 状态码
        mock_post.return_value.status_code = 500

        # 调用 send_alert 函数
        result = send_alert('test_hostname', '127.0.0.1', 'Test alert message')

        # 验证是否调用了 requests.post
        mock_post.assert_called_once()

        # 验证返回值为 False
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

