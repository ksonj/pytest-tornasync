import json
import time


import tornado.gen
import tornado.ioloop
import tornado.web

import pytest

from test import MESSAGE, PAUSE_TIME


@pytest.fixture(params=['io_loop_tornado', 'io_loop_asyncio'])
def io_loop(request):
    return request.getfuncargvalue(request.param)


@pytest.fixture
def mynumber():
    return 42


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(MESSAGE)


def _pause_coro(period):
    return tornado.gen.sleep(period)


async def pause():
    await _pause_coro(PAUSE_TIME)


def test_plain_function():
    # non-coroutine test function without fixtures
    assert True


def test_plain_function_with_fixture(mynumber):
    # non-coroutine test function that uses a fixture
    assert mynumber == 42


async def nontest(io_loop):
    # Non-test function that shouldn't be run
    assert False


async def test_pause(io_loop):
    start = time.time()
    await pause()
    elapsed = time.time() - start
    assert elapsed >= PAUSE_TIME


async def test_http_client_fetch1(http_client):
    resp = await http_client.fetch('http://httpbin.org/headers')
    assert resp.code == 200
    data = json.loads(resp.body.decode('utf8'))
    assert data == {
        'headers': {
            'Host': 'httpbin.org',
            'Accept-Encoding': 'gzip'
        }
    }


async def test_http_client_fetch2(http_client):
    resp = await http_client.fetch('http://httpbin.org/status/204')
    assert resp.code == 204


async def test_http_server_client_fetch(http_server_client):
    resp = await http_server_client.fetch('/')
    assert resp.code == 200
    assert resp.body.decode('utf8') == MESSAGE


@pytest.mark.xfail(strict=True, raises=tornado.ioloop.TimeoutError)
@pytest.mark.timeout(seconds=0.1)
async def test_timeout(io_loop):
    await _pause_coro(0.15)