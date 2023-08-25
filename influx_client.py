import keyring
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient:

    def __init__(self, org, url, access_token):
        self.access_token = access_token
        self.org = org
        self.url = url

        self.client = InfluxDBClient(
           url=self.url,
           token=self.access_token,
           org=self.org
        )

    def send_data(self, bucket, measurement, location, temperature):

        point = (
            Point(measurement)
            .tag("location", location)
            .field("temperature", temperature)
        )

        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        write_api.write(
            bucket=bucket,
            org=self.org,
            record=point
        )

    def get_data(self, bucket, range_start, measurement):

        query = (
            f'from(bucket:"{bucket}")'
            f'|> range(start: {range_start})'
            f'|> filter(fn:(r) => r._measurement == "{measurement}")'
        )

        query_api = self.client.query_api()

        result = query_api.query(
            org=self.org,
            query=query
        )

        return result.to_json()


def initiate_client():
    org = "chris-corp"
    url = "http://localhost:8086"
    access_token = keyring.get_password(
        "INFLUXDB_ACCESS",
        "influxdb"
    )

    client = InfluxClient(
        access_token=access_token,
        org=org,
        url=url
    )

    return client
