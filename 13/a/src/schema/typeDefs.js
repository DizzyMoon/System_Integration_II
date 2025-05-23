
const { gql } = require('apollo-server');

const typeDefs = gql`
  type Book {
    id: ID!
    title: String
    releaseYear: Int
    authorId: ID!
    author: Author
  }

  type Author {
    id: ID!
    name: String
    books: [Book]
  }

  type ErrorMessage {
    message: String
    errorCode: Int
  }

  type SuccessMessage {
    message: String
  }

  type Query {
    books: [Book]
    book(id: ID!): Book
    authors: [Author]
    author(id: ID!): Author
  }

  type Mutation {
    createBook(authorId: ID!, title: String!, releaseYear: Int): Book
    updateBook(id: ID!, authorId: ID, title: String, releaseYear: Int): Book
    deleteBook(id: ID!): SuccessMessage
  }

  type Subscription {
    bookAdded: Book
  }
`;

module.exports = typeDefs;
