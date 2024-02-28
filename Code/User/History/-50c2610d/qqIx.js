const mongoose = require("mongoose");
const Schema = new mongoose.Schema();

const exerciseShema = new Schema(
  {
    userName: {
      type: String,
      required: true,
      unique: true,
      minLength: 3,
    },
  },
  {description:{type: String, required: true}},
  {date:{type: Date,required: true}},
  {duration: {
    type: Number, required: true}
  },
  { timestamps: true }
);

const Exercise = mongoose.model('exerciseShema', exerciseShema);
module.exports = Exercise