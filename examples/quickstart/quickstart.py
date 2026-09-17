#!/usr/bin/env python3
"""SkyWay Python SDK クイックスタート

使い方:
    python quickstart.py [room_name]

環境変数:
    SKYWAY_APP_ID     - アプリケーションID（必須）
    SKYWAY_SECRET_KEY - シークレットキー（必須）
"""

import argparse
import asyncio
import os
import signal
import sys
import time
import uuid

import jwt

from aiortc.mediastreams import MediaStreamTrack, MediaStreamError

from skyway.room import (
    LocalRoomMember,
    SkyWayContext,
    StreamPublishedEvent,
    Publication,
    ContentType,
    LocalDataStream,
    RemoteMediaStream,
)


TOKEN_EXPIRY_SECONDS: int = 60 * 60


def _generate_auth_token() -> str:
    app_id = os.environ.get("SKYWAY_APP_ID", "")
    secret_key = os.environ.get("SKYWAY_SECRET_KEY", "")
    if not app_id or not secret_key:
        print("エラー: SKYWAY_APP_ID と SKYWAY_SECRET_KEY を設定してください。")
        sys.exit(1)
    issued_at = int(time.time())
    payload = {
        "jti": str(uuid.uuid4()),
        "iat": issued_at,
        "exp": issued_at + TOKEN_EXPIRY_SECONDS,
        "version": 3,
        "scope": {
            "appId": app_id,
            "rooms": [
                {
                    "name": "*",
                    "methods": ["create"],
                    "member": {
                        "name": "*",
                        "methods": ["publish", "subscribe"],
                    },
                },
            ],
        },
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def _receive_frames(track: MediaStreamTrack) -> None:
    frame_count = 0
    while True:
        try:
            frame = await track.recv()
            frame_count += 1
            if frame_count % 100 == 0:
                print(
                    f"[{track.kind}] Received {frame_count} frames from track {track.id}"
                )
        except MediaStreamError:
            return


async def main(room_name: str) -> None:
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, stop_event.set)
        loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    except (NotImplementedError, RuntimeError):
        pass

    receive_tasks: list[asyncio.Task[None]] = []
    context: SkyWayContext | None = None
    member: LocalRoomMember | None = None
    try:
        token = _generate_auth_token()

        context = SkyWayContext()
        await context.setup(token)

        room = await context.find_or_create_room(room_name)
        member = await room.join()

        stream = LocalDataStream()
        await member.publish(stream)

        def should_subscribe(pub: Publication) -> bool:
            return (
                pub.content_type in (ContentType.AUDIO, ContentType.VIDEO)
                and pub.publisher_id != member.id
            )

        async def _subscribe(publication_id: str) -> None:
            subscription = await member.subscribe(publication_id)
            if not isinstance(subscription.stream, RemoteMediaStream):
                return
            # 受信した映像・音声データには subscription.stream.track を通じてアクセスできます
            await _receive_frames(subscription.stream.track)

        @room.on("stream_published")
        def on_stream_published(event: StreamPublishedEvent) -> None:
            publication = room.publications.get(event.publication_id)
            if publication is None or not should_subscribe(publication):
                return
            receive_task = asyncio.create_task(_subscribe(publication.id))
            receive_tasks.append(receive_task)

        for pub in list(room.publications.values()):
            if should_subscribe(pub):
                receive_task = asyncio.create_task(_subscribe(pub.id))
                receive_tasks.append(receive_task)

        # 1秒間隔で現在のタイムスタンプを送信する
        while not stop_event.is_set():
            stream.write(str(time.time()))
            await asyncio.sleep(1)
    finally:
        for task in receive_tasks:
            task.cancel()
        await asyncio.gather(*receive_tasks, return_exceptions=True)
        if member is not None:
            try:
                await member.leave()
            except Exception as e:
                print(f"Room からの退出に失敗しました: {e}")
        if context is not None:
            await context.dispose()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SkyWay Python SDK クイックスタート")
    parser.add_argument(
        "room_name",
        nargs="?",
        default="quickstart-room",
        help="参加または作成する room 名（デフォルト: quickstart-room）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.room_name))
