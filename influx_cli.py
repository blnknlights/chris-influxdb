import click
from influx_client import initiate_client


@click.command()
@click.option('-b', '--bucket', default="chris-bucket", help='bucket name')
@click.option('-m', '--measurement', default="chris_measurement", help='measurement name')  # noqa E501
@click.option('-l', '--location', default="Prague", help='location name')
@click.option('-t', '--temperature', default=22.5, help='temperature name')
def send_data(bucket, measurement, location, temperature):
    influx = initiate_client()

    influx.send_data(
        bucket=bucket,
        measurement=measurement,
        location=location,
        temperature=temperature
    )

    influx.client.close()

    click.echo("ok")


@click.command()
@click.option('-b', '--bucket', default="chris-bucket", help='bucket name')
@click.option('-m', '--measurement', default="chris_measurement", help='measurement name')  # noqa E501
@click.option('-s', '--range_start', default="-10m", help='measurement name')
def get_data(bucket, measurement, range_start):
    influx = initiate_client()

    data = influx.get_data(
        bucket=bucket,
        measurement=measurement,
        range_start=range_start
    )

    influx.client.close()

    click.echo(data)


@click.group()
def main():
    pass


if __name__ == "__main__":
    main.add_command(get_data)
    main.add_command(send_data)
    main()
