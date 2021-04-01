import json


class InteractionResponseType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5


class InteractionResponse:
    def __init__(self, content=None, *, tts=False, embed=None, embeds=None,
                 allowed_mentions={"parse": ["roles", "users", "everyone"]},
                 deferred=False, file=None, files=None):
        self.content = content
        self.tts = tts

        if embed is not None and embeds is not None:
            raise ValueError("Specify only one of embed or embeds")
        if embed is not None:
            embeds = [embed]
        self.embeds = embeds

        if file is not None and files is not None:
            raise ValueError("Specify only one of file or files")
        if file is not None:
            files = [file]
        self.files = files

        self.allowed_mentions = allowed_mentions

        if deferred:
            self.response_type = \
                InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
        else:
            self.response_type = \
                InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE

        if (self.content is None and self.embeds is None
                and self.files is None and not deferred):
            raise ValueError(
                "Supply at least one of content, embeds, files, or deferred.")

    @staticmethod
    def from_return_value(result):
        if result is None:
            return InteractionResponse()
        elif isinstance(result, InteractionResponse):
            return result
        else:
            return InteractionResponse(str(result))

    def dump(self):
        return {
            "type": self.response_type,
            "data": {
                "content": self.content,
                "tts": self.tts,
                "embeds": self.embeds,
                "allowed_mentions": self.allowed_mentions
            }
        }

    def dump_followup(self):
        return {
            "content": self.content,
            "tts": self.tts,
            "embeds": self.embeds,
            "allowed_mentions": self.allowed_mentions
        }

    def dump_multipart(self):
        if self.files:
            payload_json = json.dumps(self.dump_followup())

            multipart = []
            for file in self.files:
                multipart.append(("file", file))

            return {"data": {"payload_json": payload_json}, "files": multipart}
        else:
            return {"json": self.dump_followup()}
