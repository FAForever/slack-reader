from flask import Blueprint, jsonify

from app.libs.slack import slack

index = Blueprint('index', __name__)


@index.route('', methods=["GET"])
def info():
    channels = slack.get_channels()
    public_channels = {channel_info["id"]: channel_info for channel_info in channels if not channel['is_archived']}
    return jsonify({
        'users': slack.get_users(),
        'channels': public_channels
    })

# TODO: if these routes get too extensive, move them to their own blueprint


@index.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    return jsonify(slack.get_user(user_id))


@index.route('/channels/<channel_id>', methods=['GET'])
def channel(channel_id):
    channel_info = slack.get_channel(channel_id)
    archived = bool(channel_info['is_archived'])
    channel_info = channel_info if not archived else {}
    return jsonify({
        'archived': archived,
        'channel': channel_info
    })


@index.route('/channels/<channel_id>/messages', methods=['GET'])
def channel_messages(channel_id):
    if slack.get_channel(channel)['is_archived']:
        return jsonify({'message': 'Archived channels are not accessible'}), 401
    return slack.get_history(channel_id, count=250)
