"""Ports `AudioController` + `routes/web.php`'s `admin.audio.*` JSON
endpoints. No Azure-key branch (and therefore no 422) — edge-tts needs no
API key; a synthesis failure is asynchronous (the worker sets
`audio_status='failed'`), surfaced only through `status`. `InvalidAudioTransitionError`
(already-processing / not-processing) is handled by the global exception
handler, which returns 409 — the only non-2xx code the admin JS reads."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.application.use_cases.audio.cancel_audio_generation import CancelAudioGeneration
from admirable.application.use_cases.audio.get_audio_status import GetAudioStatus
from admirable.application.use_cases.audio.request_audio_generation import RequestAudioGeneration
from admirable.presentation.web.dependencies import (
    get_cancel_audio_generation_uc,
    get_get_audio_status_uc,
    get_request_audio_generation_uc,
    require_auth,
)

router = APIRouter(prefix="/admin/audio", dependencies=[Depends(require_auth)])

_Kind = Literal["figure", "story"]


@router.post("/generate/{kind}/{id}", name="admin.audio.generate")
async def generate(
    kind: _Kind,
    id: int,
    use_case: Annotated[RequestAudioGeneration, Depends(get_request_audio_generation_uc)],
) -> object:
    await use_case.execute(AudioActionCommand(kind=kind, entity_id=id))
    return JSONResponse({"message": "Audio generation has been queued."})


@router.post("/cancel/{kind}/{id}", name="admin.audio.cancel")
async def cancel(
    kind: _Kind,
    id: int,
    use_case: Annotated[CancelAudioGeneration, Depends(get_cancel_audio_generation_uc)],
) -> object:
    await use_case.execute(AudioActionCommand(kind=kind, entity_id=id))
    return JSONResponse({"message": "Audio generation has been cancelled."})


@router.get("/status/{kind}/{id}", name="admin.audio.status")
async def status(
    kind: _Kind,
    id: int,
    use_case: Annotated[GetAudioStatus, Depends(get_get_audio_status_uc)],
) -> object:
    result = await use_case.execute(AudioActionCommand(kind=kind, entity_id=id))
    return JSONResponse(
        {"status": result.status.value, "error": result.error, "audio_url": result.audio_url}
    )
