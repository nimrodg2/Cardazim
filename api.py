from card_manager import *
import argparse
import flask

app = flask.Flask(__name__)
cm: CardManager = None


@app.route('/creators', methods=['GET'])
def get_creators():
    return flask.render_template("show_list.html", lst=cm.GetCreators())


@app.route('/creators/<creator>/cards/solved', methods=['GET'])
def get_creators_solved_cards(creator: str):
    data = cm.GetCreatorCards(creator)
    data = [card for card in data if card.solution is not None]
    return flask.render_template("show_list.html", lst=data)


@app.route('/creators/<creator>/cards/unsolved', methods=['GET'])
def get_creators_unsolved_cards(creator: str):
    data = cm.GetCreatorCards(creator)
    data = [card for card in data if card.solution is None]
    return flask.render_template("show_list.html", lst=data)


@app.route('/creators/<creator>/cards/<card_name>', methods=['GET'])
def get_creators_card_names(creator, name):
    identity = name + "_" + creator
    card: Card = cm.load(identity)
    return flask.render_template("show_list.html", lst=[card.name, card.creator, card.path, card.riddle, card.solution])


@app.route('/creators/<creator>/cards/<card_name>/image.jpg', methods=['GET'])
def get_image(creator, name):
    identity = name + "_" + creator
    card: Card = cm.load(identity)
    return flask.render_template("image.html", path=card.path)


@app.route('/cards/find', methods=['GET'])
def get_cards():
    try:
        name = flask.request.args.get("name")
    except:
        name = "*"
    try:
        creator = flask.request.args.get("creator")
    except:
        creator = "*"
    try:
        riddle = flask.request.args.get("riddle")
    except:
        riddle = "*"
    return flask.render_template("show_list.html", lst=cm.get_card_something(creator, name, riddle))


# THERE IS NO SUCH THING AS CARD ID SO I TOOK SOME CREATIVE LIBERTIES
@app.route('/creators/<creator>/cards/<card_name>/<solution>', methods=['POST'])
def solve(creator, card_name, solution):
    identity = card_name + "_" + creator
    card: Card = cm.load(identity)
    if card.image.decrypt(solution):
        cm.Update_solution(creator, card_name, solution)
        return flask.render_template("show_list.html", title="solution is correct", lst="")
    else:
        return flask.render_template("show_list.html", title="solution is wrong", lst="")


def run_server(ip: str, port: str):
    app.run(ip, port)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('path', type=str,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    global cm
    args = get_args()
    dbm = DatabaseManager()
    cm = CardManager(dbm)
    run_server(args.ip, args.port)


if __name__ == '__main__':
    main()
