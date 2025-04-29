from types import SimpleNamespace
from src.utils.keyboard import create_keybord, create_inline_keyboard


keys = SimpleNamespace(
    pdf=':page_facing_up: PDF',
    settings=':gear: Settigs',
    audio=':headphone: Audio',
    back=':BACK_arrow: Back',
    account=':bust_in_silhouette: Account',
    enable_transcription=':check_mark: Enable transcription',
    disable_transcription=':cross_mark: Disable transcription',
    enable_prompt=':check_mark: Enable prompt',
    disable_prompt=':cross_mark: Disable prompt',
)

keyboards = SimpleNamespace(
                            main=create_keybord(keys.settings, keys.account),
                            main_inline=create_inline_keyboard(keys.pdf, keys.audio),
                            voice = create_inline_keyboard(keys.enable_transcription, keys.disable_transcription, keys.enable_prompt, keys.disable_prompt, keys.back)
                            )

states = SimpleNamespace(
    transcript= False,
    voice=False,
    voice_prompt=False,)