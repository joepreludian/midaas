import pytest
import vcr


@pytest.fixture(scope="session")
def ensure_mocked_http_client(request):
    root_path = request.config.rootdir

    def avoid_capture_localstack_calls(request):
        if request.host == "localstack":
            return None

        return request

    vcr_instance = vcr.VCR(before_record_request=avoid_capture_localstack_calls)
    with vcr_instance.use_cassette(
        f"{root_path}/tests/vcr_calls.yaml",
        serializer="yaml",
        record_mode="new_episodes",
        filter_headers=["access_token"],
        match_on=["method", "scheme", "host", "port", "path", "query", "body"]
    ):
        yield
