import sentry_sdk


"""Sentry Integration class for handling Sentry SDK operations."""


class SentryIntegration:
    def __init__(self, dsn_url, default_pii, traces_sample_rate, profiles_sample_rate):
        """Initialize the Sentry Integration.

        @param dsn_url: The DSN URL for the Sentry Integration
        @param default_pii: Whether to send default PII data
        @param traces_sample_rate: The sample rate for traces
        @param profiles_sample_rate: The sample rate for profiles
        """
        sentry_sdk.init(
            dsn=dsn_url,
            send_default_pii=default_pii,
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            debug=False,
        )

    def set_context(self, payload):
        """Set the context for the Sentry Integration.

        @param payload: The payload to set the context for
        """
        sentry_sdk.set_context("custom_data", payload)

    def capture_message(self, message, level):
        """Capture a message for the Sentry Integration.

        @param message: The message to capture
        @param level: The level of the message
        """
        sentry_sdk.capture_message(message=message, level=level)

    def flush(self):
        """Flush the Sentry Integration."""
        sentry_sdk.flush()


"""Base class for all Sentry payload types. This is inherited by all other payload types."""


class BaseSentryPayload():
    def __init__(self):
        """Initialize the Base Sentry Payload."""
        self.data = {}

    def set_redcoffee_version(self, red_coffee_version):
        """Set the Red Coffee Version.

        @param red_coffee_version: The version of Red Coffee
        """
        self.data["redcoffee_version"] = red_coffee_version

    def set_operating_system(self, operating_system):
        """Set the Operating System.

        @param operating_system: The operating system
        """
        self.data["operating_system"] = operating_system

    def set_country_of_origin(self, country_of_origin):
        """Set the Country of Origin.

        @param country_of_origin: The country of origin
        """
        self.data["country_of_origin"] = country_of_origin

    def get_data(self):
        """Get the Data."""
        return self.data


"""Payload class for handling general unsuccessful operations."""


class SentryGeneralUnsuccessfulPayload(BaseSentryPayload):
    def set_sonarqube_version(self, sonarqube_version):
        """Set the SonarQube Version.

        @param sonarqube_version: The version of SonarQube
        """
        self.data["sonarqube_version"] = sonarqube_version

    def set_major_programming_language(self, major_programming_language):
        """Set the Major Programming Language.

        @param major_programming_language: The major programming language
        """
        self.data["major_programming_language"] = major_programming_language

    def set_response_code(self, response_code):
        """Set the Response Code.

        @param response_code: The response code
        """
        self.data["response_code"] = response_code

    def set_is_user_token(self, is_user_token):
        """Set the Is User Token.

        @param is_user_token: Whether the token is a user token
        """
        self.data["is_user_token"] = is_user_token


"""Payload class for handling unsuccessful connection operations."""


class SentryConnectionUnsuccessfulPayload(BaseSentryPayload):
    def set_protocol(self, protocol):
        """Set the Protocol.

        @param protocol: The protocol
        """
        self.data["protocol"] = protocol

    def set_assigned_protocol_type(self, assigned_protocol_type):
        """Set the Assigned Protocol Type.

        @param assigned_protocol_type: The assigned protocol type
        """
        self.data["assigned_protocol_type"] = assigned_protocol_type


"""Payload class for handling successful general operations."""


class SentryGeneralSuccessPayload(BaseSentryPayload):
    def set_sonarqube_version(self, sonarqube_version):
        """Set the SonarQube Version."""
        self.data["sonarqube_version"] = sonarqube_version

    def set_major_programming_language(self, major_programming_language):
        """Set the Major Programming Language."""
        self.data["major_programming_language"] = major_programming_language
