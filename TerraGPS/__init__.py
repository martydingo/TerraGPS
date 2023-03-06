import requests, logging, logging.handlers, argparse
from ttf_opensans import opensans
from PIL import Image, ImageDraw, ImageFont


class TerraGPS:
    def __init__(
        self, tshock_token, tshock_host, input_image, output_image, tshock_port=7878
    ):
        self.initLogging()
        self.token = tshock_token
        self.uri = f"http://{tshock_host}:{tshock_port}"
        self.log.debug(
            f"TerrariaGPS: Initializing with token {self.token} and uri {self.uri}"
        )
        self.paintPlayersontoImage(input_image, output_image)

    def initLogging(self):
        self.log = logging.getLogger("TerrariaGPS")

        logFormatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        stdoutStreamHandler = logging.StreamHandler()
        stdoutStreamHandler.setFormatter(logFormatter)
        syslogStreamHandler = logging.handlers.SysLogHandler()
        syslogStreamHandler.setFormatter(logFormatter)

        self.log.setLevel(logging.DEBUG)

        self.log.addHandler(stdoutStreamHandler)
        self.log.addHandler(syslogStreamHandler)

        self.log.debug("Logging Initialized")

    def getPlayers(self):
        r = requests.get(f"{self.uri}/v2/players/list?token={self.token}")
        if r.status_code == 200:
            usernameArray = []
            for player in r.json()["players"]:
                usernameArray.append(player["username"])
            return usernameArray
        else:
            self.log.error(f"Error getting players from Terraria server: {r.json()}")
            return []

    def getPosition(self, player):
        r = requests.get(
            f"{self.uri}/v4/players/read?player={player}&token={self.token}"
        )
        if r.status_code == 200:
            position = r.json()["position"]
            return {"X": int(position.split(",")[0]), "Y": int(position.split(",")[1])}
        else:
            if r.status_code == 400:
                self.log.error(f"{player} could not be found on the Terraria server")
            else:
                self.log.error(
                    f"Error getting position of {player} from Terraria server: {r.json()}"
                )

    def paintPlayersontoImage(self, input_image, output_image):
        fontSize = 16
        font = opensans().imagefont(size=fontSize)
        image = Image.open(input_image)
        for player in self.getPlayers():
            position = self.getPosition(player)
            if position:
                draw = ImageDraw.Draw(image)
                draw.ellipse(
                    (
                        position["X"] - 6.25,
                        position["Y"] - 6.25,
                        position["X"] + 6.25,
                        position["Y"] + 6.25,
                    ),
                    outline="red",
                )
                draw.text(
                    (
                        position["X"] - len(player) * fontSize / 4,
                        position["Y"] - 3.125 + (fontSize / 4),
                    ),
                    text=player,
                    fill="black",
                    font=font,
                )
        image.save(output_image)


if __name__ == "__main__":
    preArgs = argparse.ArgumentParser(
        prog="TerrariaGPS",
        description="A simple class to get the position of a player in Terraria via the Terraria API and paint it onto the world image",
    )
    preArgs.add_argument("-h", "--host", help="The host of the Terraria server")
    preArgs.add_argument(
        "--port",
        help="The port of the Terraria server",
        default=7878,
    )
    preArgs.add_argument("-t", "--token", help="The token of the Terraria server")
    preArgs.add_argument(
        "-i",
        "--input_image",
        help="The world image to paint the players on",
    )
    preArgs.add_argument(
        "-o",
        "--output_image",
        help="The world image to paint the players on",
    )

    args = preArgs.parse_args()

    terrariaGPS = TerraGPS(
        tshock_token=args.token,
        tshock_host=args.host,
        tshock_port=args.port,
        input_image=args.input_image,
        output_image=args.output_image,
    )
