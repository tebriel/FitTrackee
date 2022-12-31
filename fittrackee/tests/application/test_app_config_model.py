import pytest
from flask import Flask

from fittrackee import VERSION
from fittrackee.application.models import AppConfig
from fittrackee.users.models import User


class TestConfigModel:
    def test_application_config(
        self, app: Flask, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv('WEATHER_API_PROVIDER', 'darksky')
        app_config = AppConfig.query.first()
        app_config.admin_contact = 'admin@example.com'

        assert app_config.is_registration_enabled is True
        assert (
            app_config.map_attribution
            == app.config['TILE_SERVER']['ATTRIBUTION']
        )

        serialized_app_config = app_config.serialize()
        assert (
            serialized_app_config['admin_contact'] == app_config.admin_contact
        )
        assert (
            serialized_app_config['gpx_limit_import']
            == app_config.gpx_limit_import
        )
        assert serialized_app_config['is_email_sending_enabled'] is True
        assert serialized_app_config['is_registration_enabled'] is True
        assert (
            serialized_app_config['max_single_file_size']
            == app_config.max_single_file_size
        )
        assert (
            serialized_app_config['max_zip_file_size']
            == app_config.max_zip_file_size
        )
        assert serialized_app_config['max_users'] == app_config.max_users
        assert (
            serialized_app_config['map_attribution']
            == app_config.map_attribution
        )
        assert serialized_app_config['version'] == VERSION
        assert serialized_app_config['weather_provider'] == 'darksky'

    def test_it_returns_registration_disabled_when_users_count_exceeds_limit(
        self, app: Flask, user_1: User, user_2: User
    ) -> None:
        app_config = AppConfig.query.first()
        app_config.max_users = 2
        serialized_app_config = app_config.serialize()

        assert app_config.is_registration_enabled is False
        assert serialized_app_config['is_registration_enabled'] is False

    def test_it_returns_email_sending_disabled_when_no_email_url_provided(
        self, app_wo_email_activation: Flask, user_1: User, user_2: User
    ) -> None:
        app_config = AppConfig.query.first()
        serialized_app_config = app_config.serialize()

        assert serialized_app_config['is_email_sending_enabled'] is False

    @pytest.mark.parametrize(
        'input_weather_api_provider, expected_weather_provider',
        [
            ('darksky', 'darksky'),
            ('Visualcrossing', 'visualcrossing'),
            ('invalid_provider', None),
            ('', None),
        ],
    )
    def test_it_returns_weather_provider(
        self,
        app: Flask,
        input_weather_api_provider: str,
        expected_weather_provider: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv('WEATHER_API_PROVIDER', input_weather_api_provider)
        app_config = AppConfig.query.first()
        serialized_app_config = app_config.serialize()

        assert (
            serialized_app_config['weather_provider']
            == expected_weather_provider
        )
