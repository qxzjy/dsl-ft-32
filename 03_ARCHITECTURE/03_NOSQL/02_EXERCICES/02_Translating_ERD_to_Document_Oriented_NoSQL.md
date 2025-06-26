# Translating an ERD to a Document-Oriented NoSQL Model 🧃

In this exercise, you will translate an ERD (entity-relationship diagram) to a document-oriented NoSQL model. You will need to identify the entities, attributes, and relationships in the ERD and map them to a document-oriented data model. You will also need to decide how to represent relationships between entities, such as by using embedded documents or references.

**Entities** :
- User
- Order
- Product
- Category

**Relationships** :
- User to Order: One-to-Many
- Product to Category: Many-to-One

## Instructions
- Identify the entities in the ERD and translate them into documents for a document-oriented NoSQL database.
- Identify the relationships between entities and decide how to represent them in the NoSQL model, using embedded documents or references.
- Define the primary keys and attributes for each document, based on the attributes of the corresponding entity in the ERD.
- Define any indexes that may be needed to support queries on the data.
- Define any validation rules or integrity constraints that should be enforced on the data.
- Choose an appropriate document-oriented NoSQL database to store the documents created from the ERD.

## Document Structure:

**Relationships**:
- User to Order: One-to-Many (embedded documents)
- Product to Category: Many-to-One (references)

User:
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  orders:
    [
      {
        _id: ObjectId,
        date: Date,
        products:
          [{ _id: ObjectId, name: String, price: Number, quantity: Number }],
      },
    ],
}
```

Order:
```javascript
{
    _id: ObjectId,
    date: Date,
    user_id: ObjectId,
    products: [
        {
            _id: ObjectId,
            name: String,
            price: Number,
            quantity: Number
        }
    ]
}
```

Product:
```javascript
{
    _id: ObjectId,
    name: String,
    price: Number,
    category_id: ObjectId
}
```

Category:
```javascript
{
    _id: ObjectId,
    name: String
}
```

## Indexes:
```javascript
User: { email: 1 }
Order: { user_id: 1, date: -1 }
Product: { name: 1 }
Category: { name: 1 }
```

## Validation rules:
- User: name and email are required, email must be unique
- Order: date is required, user_id must reference a valid user
- Product: name and price are required, category_id must reference a valid category
- Category: name is required
- Document-oriented NoSQL database: MongoDB
