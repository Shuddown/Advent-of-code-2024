"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs_1 = require("fs");
function countOccurences(array, target) {
    var count = 0;
    for (var _i = 0, array_1 = array; _i < array_1.length; _i++) {
        var elem = array_1[_i];
        if (elem === target)
            count += 1;
    }
    return count;
}
(0, fs_1.readFile)('input.txt', 'utf-8', function (err, data) {
    if (err) {
        console.log("Failed to read input");
        console.log(err);
        return;
    }
    var re = /\s+/;
    var strings = data.split(re);
    var column1 = strings.filter(function (string, index) { return index % 2 === 0; });
    var column2 = strings.filter(function (string, index) { return index % 2 === 1; });
    var nums1 = column1.map(function (value) { return parseInt(value, 10); });
    var nums2 = column2.map(function (value) { return parseInt(value, 10); });
    nums1.sort(function (a, b) { return a - b; });
    nums2.sort(function (a, b) { return a - b; });
    var distances = nums1.map(function (value, index) { return Math.abs(value - nums2[index]); });
    var total_distance = distances.reduce(function (acc, value) { return acc + value; }, 0);
    var similarity_score = nums1.map(function (value) { return value * countOccurences(nums2, value); }).reduce(function (acc, value) { return acc + value; }, 0);
    console.log(total_distance);
    console.log(similarity_score);
});
