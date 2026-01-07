Section A: Limitations of RDBMS

Relational Database Management Systems (RDBMS) are designed around a fixed, predefined schema, which makes them less suitable for handling highly heterogeneous data. In the FlexiMart product catalog, different product categories require different attributes. For example, electronic products such as laptops require attributes like processor and RAM, whereas fashion products require attributes such as size, color, and material. Modeling such variability in an RDBMS leads to excessive NULL values or complex table structures.

RDBMS systems also struggle with frequent schema evolution. Introducing new product attributes requires schema alterations using ALTER TABLE, which is an expensive operation and can impact system availability. This reduces agility when onboarding new product types.

Additionally, storing customer reviews in a relational model requires separate tables and foreign key relationships. Retrieving product information along with reviews involves multiple JOIN operations, increasing query complexity and reducing performance as data volume grows.
________________________________________________________________________________________________________________________________
Section B: NoSQL Benefits

MongoDB, as a document-oriented NoSQL database, overcomes these limitations by supporting a flexible schema model. Each product can be stored as a self-contained document, allowing different products to have different sets of attributes without schema modification. This approach aligns well with dynamic and evolving product catalogs.

MongoDB also supports embedded documents, enabling customer reviews to be stored directly within the product document. This eliminates the need for JOIN operations and allows efficient retrieval of products along with their associated reviews in a single query.

Furthermore, MongoDB is designed for horizontal scalability. It supports sharding, which allows data to be distributed across multiple nodes. This makes MongoDB suitable for large-scale applications with growing data volume and high read/write throughput, such as an expanding e-commerce product catalog.

______________________________________________________________________________________________________________________________

Section C: Trade-offs 

One limitation of MongoDB compared to relational databases is reduced support for complex multi-entity transactions. While MongoDB provides transaction support, RDBMS systems offer more mature ACID guarantees for transactional workloads.

Another trade-off is the lack of enforced schema constraints at the database level. MongoDB follows a schema-less design, which places responsibility for data validation on the application layer. Without proper validation mechanisms, this can result in inconsistent document structures and data quality issues over time.