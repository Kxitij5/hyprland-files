const mongoose = require("mongoose");
const Schema = new mongoose.Schema();

const userSchema = new Schema(
  {
    userName: {
      type: String,
      required: true,
      unique: true,
      minLength: 3,
    },
  },
  { age: { type: Number, required: true } },
  { timestamps: true }
);

const User = mongoose.model('user', userSchema);
module.exports = User;