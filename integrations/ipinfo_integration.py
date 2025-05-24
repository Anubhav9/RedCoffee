import logging

import ipinfo


"""Integration class for handling IPInfo operations and geolocation lookups."""


class IPInfoIntegration:
    def __init__(self, api_key):
        """Initialize IPInfo integration with API key.
        @param api_key: The API key for IPInfo service
        """
        self.api_key = api_key
        self.default_country = "Default Location - North Korea"

    def get_user_geo_location(self):
        """Get the user's country based on their IP address.
        Returns:
            str: Two-letter country code or default location on error
        """
        try:
            handler = ipinfo.getHandler(self.api_key)
            details = handler.getDetails()
            user_country = details.country
            return user_country
        except Exception as e:
            logging.info(
                f"Something went wrong with IPInfo Integration with exception as :: {e}")
            return self.default_country
