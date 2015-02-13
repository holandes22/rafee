from rest_framework import status


def assert_status_and_items_equal(expected_code, expected, response):
    actual = response.data
    assert expected_code == response.status_code
    assert len(actual) == len(expected)
    assert sorted(actual) == sorted(expected)


def assert_200_and_items_equal(expected, response):
    return assert_status_and_items_equal(
        status.HTTP_200_OK,
        expected,
        response,
    )


def assert_201_and_items_equal(expected, response):
    return assert_status_and_items_equal(
        status.HTTP_201_CREATED,
        expected,
        response,
    )
