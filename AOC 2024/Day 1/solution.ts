import { readFile } from "fs";


function countOccurences<T>(array: T[], target: T): number {
    let count = 0;
    for(let elem of array){
        if (elem === target) count += 1;
    }
    return count;
}

readFile('input.txt', 'utf-8', (err, data) => {
    if (err) {
        console.log("Failed to read input");
        console.log(err);
        return;
    }
    const re: RegExp = /\s+/;
    const strings: string[] = data.split(re);
    const column1: string[] = strings.filter((string, index) => index % 2 === 0);
    const column2: string[] = strings.filter((string, index) => index % 2 === 1);
    const nums1: number[] = column1.map((value) => parseInt(value, 10));
    const nums2: number[] = column2.map((value) => parseInt(value, 10));
    nums1.sort((a, b) => a - b);
    nums2.sort((a, b) => a - b);

    const distances: number[] = nums1.map((value, index) => Math.abs(value - nums2[index]));
    const total_distance: number =  distances.reduce((acc, value) => acc + value, 0);
    const similarity_score = nums1.map((value) => value * countOccurences(nums2, value)).reduce((acc, value) => acc + value, 0);
    console.log(total_distance);
    console.log(similarity_score);
});


