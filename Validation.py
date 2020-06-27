"""A framework for validating various kinds of values."""

from abc import ABCMeta, abstractmethod

import typing


class _Operator(metaclass=ABCMeta):
    """An ABC for any object that validates things."""

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def invalidity_reasons(self) -> str:
        raise NotImplementedError


class Chain(_Operator):
    """Evaluates a chain of validators.

    Indicates invalidity if any validator passed in the constructor indicates
    invalidity. The invalidity reasons are a list of reasons returned by the
    individual validators.
    """

    def __init__(self, validators: typing.List[_Operator]):

        if len(validators) == 0:
            raise ValueError

        # If any validator indicates invalidity the whole chain will indicate
        # invalidity.
        self._is_valid = True
        self._invalidity_reasons = ''
        for validator in validators:
            if not validator.is_valid():
                self._is_valid = False
                self._invalidity_reasons += validator.invalidity_reasons

    def is_valid(self) -> bool:
        return self._is_valid

    def invalidity_reasons(self) -> str:
        return self._invalidity_reasons


class _FeedbackTemplates:

    WAS_SMALLER_THAN_THRESHOLD = (
        'The value "{0}" should have been greater than or equal to {1}, but '
        'was {2} instead.\n')
    WAS_SMALLER_THAN_OR_EQUAL_TO_THRESHOLD = (
        'The value "{0}" should have been greater than {1}, but was {2} '
        'instead.\n')
    WAS_GREATER_THAN_THRESHOLD = (
        'The value "{0}" should have been smaller than or equal to {1}, but '
        'was {2} instead.\n')
    WAS_GREATER_THAN_OR_EQUAL_TO_THRESHOLD = (
        'The value "{0}" should have been smaller than {1}, but was {2} '
        'instead.\n')
    WAS_NOT_IN_SET = (
        'The value "{0}" = {1} was not among the values in:\n{2}.\n'
    )

    @staticmethod
    def print_set(values: typing.Set) -> str:

        assert (len(values) > 0)

        value_strings = [str(value) for value in values]
        value_string_lengths = [len(value_string) for value_string in value_strings]

        # maximum line length should be 80 characters
        return '[' + ', '.join(value_strings) + ']'


class LowerThan(_Operator):

    def __init__(self,
                 value,
                 name: str,
                 threshold,
                 or_equal_to: bool = False
                 ):

        assert (isinstance(value, (int, float)))
        assert (isinstance(threshold, (int, float)))
        assert (name is not '')

        self._invalidity_reason = ''

        if or_equal_to:
            if value > threshold:
                self._invalidity_reason = _FeedbackTemplates.\
                    WAS_GREATER_THAN_THRESHOLD
        else:
            if value >= threshold:
                self._invalidity_reason = _FeedbackTemplates.\
                    WAS_GREATER_THAN_OR_EQUAL_TO_THRESHOLD

        if self._invalidity_reason is not '':
            self._invalidity_reason.format(name, threshold, value)
            self._is_valid = False
        else:
            self._is_valid = True

    def is_valid(self) -> bool:
        return self._is_valid

    def invalidity_reasons(self) -> str:
        return self._invalidity_reason


class GreaterThan(_Operator):

    def __init__(self,
                 value,
                 name: str,
                 threshold,
                 or_equal_to: bool = False
                 ):

        assert (isinstance(value, (int, float)))
        assert (isinstance(threshold, (int, float)))
        assert (name is not '')

        self._invalidity_reason = ''

        if or_equal_to:
            if value < threshold:
                self._invalidity_reason = _FeedbackTemplates.\
                    WAS_SMALLER_THAN_THRESHOLD
        else:
            if value <= threshold:
                self._invalidity_reason = _FeedbackTemplates.\
                    WAS_SMALLER_THAN_OR_EQUAL_TO_THRESHOLD

        if self._invalidity_reason is not '':
            self._invalidity_reason.format(name, threshold, value)
            self._is_valid = False
        else:
            self._is_valid = True

    def is_valid(self) -> bool:
        return self._is_valid

    def invalidity_reasons(self) -> str:
        return self._invalidity_reason


class OneOf(_Operator):

    def __init__(self,
                 value,
                 name: str,
                 values: typing.Set
                 ):
        if value not in values:
            self._is_valid = False
            self._invalidity_reason = \
                _FeedbackTemplates.WAS_NOT_IN_SET.format(
                    name, value, _FeedbackTemplates.print_set(values)
                )
        else:
            self._is_valid = True
            self._invalidity_reason = ''

    def is_valid(self) -> bool:
        return self._is_valid

    def invalidity_reasons(self) -> str:
        return self._invalidity_reason


class CanBeOfType(_Operator):
    """I don't know how to do this yet."""
