const { books, authors } = require('../data/db');
const pubsub = require('../subscriptions/pubsub');
const BOOK_ADDED = 'BOOK_ADDED';

const resolvers = {
  Query: {
    books: () => books,
    book: (_, { id }) => books.find(b => b.id === id),
    authors: () => authors,
    author: (_, { id }) => authors.find(a => a.id === id),
  },
  Mutation: {
    createBook: (_, { authorId, title, releaseYear }) => {
      const book = {
        id: String(books.length + 1),
        title,
        releaseYear,
        authorId
      };
      books.push(book);
      pubsub.publish(BOOK_ADDED, { bookAdded: book });
      return book;
    },
    updateBook: (_, { id, ...updates }) => {
      const index = books.findIndex(b => b.id === id);
      if (index === -1) return null;
      books[index] = { ...books[index], ...updates };
      return books[index];
    },
    deleteBook: (_, { id }) => {
      const index = books.findIndex(b => b.id === id);
      if (index === -1) return { message: 'Book not found' };
      books.splice(index, 1);
      return { message: 'Book deleted successfully' };
    }
  },
  Subscription: {
    bookAdded: {
      subscribe: () => pubsub.asyncIterator([BOOK_ADDED])
    }
  },
  Book: {
    author: (book) => authors.find(a => a.id === book.authorId)
  },
  Author: {
    books: (author) => books.filter(b => b.authorId === author.id)
  }
};

module.exports = resolvers;
