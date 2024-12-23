class TestBase:
    def test_health(self, http_client):
        response = http_client.get("/health/")
        assert response.status_code == 200
        response_payload = response.json()

        assert response_payload['status'] == 'healthy'
        assert response_payload['remarks'] == []
        assert response_payload['asaas_root_account_status']['general'] == 'APPROVED'
