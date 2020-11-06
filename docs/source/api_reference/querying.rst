Querying
================

.. automodule:: quickbase_client.orm

.. toctree::
   :maxdepth: 2
   :caption: Contents:


QueryBase
---------------

.. autoclass:: quickbase_client.QuickBaseQuery
    :members:
    :undoc-members:

|


AST Query Building Methods
--------------------------

.. automodule:: quickbase_client.query.ast

.. automodule:: quickbase_client.query

    .. py:function:: or_(*clauses)

        Conjunction to join 2 or more logical ``OR``'s.

    .. py:function:: and_(*clauses)

        Conjunction to join 2 or more logical ``AND``'s.

    .. py:function:: contains_(field, val)

        Contains (CT).

    .. py:function:: not_contains_(field, val)

        Not Contains (XCT).

    .. py:function:: has_(field, val)

        Has (HAS).

    .. py:function:: not_has_(field, val)

        Not Has (XHAS).

    .. py:function:: eq_(field, val)

        Equal/Exactly (EX).

    .. py:function:: not_eq_(field, val)

        Not Equal (XEX).

    .. py:function:: starts_with_(field, val)

        Starts With (SW).

    .. py:function:: not_starts_width_(field, val)

        Not Starts With (XSW).

    .. py:function:: before_(field, val)

        Before (BF).

    .. py:function:: on_or_before_(field, val)

        On or Before (OBF).

    .. py:function:: after_(field, val)

        After (AF).

    .. py:function:: on_or_after_(field, val)

        On or After (OAF).

    .. py:function:: during_(field, val)

        During (IR).

    .. py:function:: not_during_(field, val)

        Not During (XIR).

    .. py:function:: lt_(field, val)

        Less than (LT).

    .. py:function:: lte_(field, val)

        Less than or Equal (LTE).

    .. py:function:: gt_(field, val)

        Greater than (GT).

    .. py:function:: gte_(field, val)

        Greater than or Equal (GTE).
