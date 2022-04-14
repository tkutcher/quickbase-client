==========
CHANGELOG
==========

`0.5.0`_ (2022-4-14)
---------------------

* Update development dependencies and better pytest practices for mocks/spies (`#54`_)
* Rename ``QuickBase-`` class prefixes to ``Quickbase-`` and make aliases  (`#54`_)
* Add Python 3.9 & 3.10 as tested python versions.


`0.4.0`_ (2021-6-30)
---------------------

* Sorting fields in ``model-generate`` to enforce deterministic order  (`#45`_) [Credit: `@mklaber`_]
* Option to normalize unicode to remove characters that aren't rendered when posted as data through the API  (`#47`_)
* Serializing datetime fields as dates when the Quickbase field is a date  (`#47`_)


`0.3.1`_ (2021-6-18)
---------------------

* Don't make unnecessary calls for skipped tables in ``model-generate`` (`#44`_)


`0.3.0`_ (2021-6-15)
---------------------

* Fix the formula strings in output ``model-generate`` files (`#38`_) [Credit: `@mklaber`_]
* Add ``--include``/``-i`` options to ``model-generate`` (`#40`_) [Credit: `@mklaber`_]
* Contributing documentation updates (`#41`_)


`0.2.0`_ (2021-4-14)
---------------------

* Include QuickbaseLogHandler tool for sending logs to Quickbase (`#28`_)
* Include RequestPaginator for managing paginated requesting (`#34`_)




`0.1.0`_ (2020-11-10)
---------------------

* Initial release
* Initial table client and API client for the JSON API
* Initial query building features
* Initial ORM between QuickBase tables and Python objects
* Initial scripts which generate model classes


..
   Tags


.. _`0.1.0`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.1.0
.. _`0.2.0`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.2.0
.. _`0.3.0`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.3.0
.. _`0.3.1`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.3.1
.. _`0.4.0`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.4.0
.. _`0.5.0`: https://github.com/tkutcher/quickbase-client/releases/tag/v0.5.0


..
   Issues


.. _`#28`: https://github.com/tkutcher/quickbase-client/issues/28
.. _`#34`: https://github.com/tkutcher/quickbase-client/issues/34
.. _`#38`: https://github.com/tkutcher/quickbase-client/issues/38
.. _`#40`: https://github.com/tkutcher/quickbase-client/issues/40
.. _`#41`: https://github.com/tkutcher/quickbase-client/issues/41
.. _`#44`: https://github.com/tkutcher/quickbase-client/issues/44
.. _`#45`: https://github.com/tkutcher/quickbase-client/issues/45
.. _`#47`: https://github.com/tkutcher/quickbase-client/issues/47
.. _`#54`: https://github.com/tkutcher/quickbase-client/issues/54


..
   Contributors


.. _`@mklaber`: https://github.com/mklaber


