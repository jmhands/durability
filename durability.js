function choose(n, r) {
    let result = 1;
    for (let i = 0; i < r; i++) {
        result *= (n - i) / (i + 1);
    }
    return result;
}

function calculateDurability() {
    const numDataShards = parseInt(document.getElementById('dataShards').value);
    const numParityShards = parseInt(document.getElementById('parityShards').value);
    const afr = parseFloat(document.getElementById('afr').value) / 100;
    const rebuildTime = parseFloat(document.getElementById('rebuildTime').value);
    const totalObjects = parseInt(document.getElementById('totalObjects').value);
    
    const yr = 365.25 * 24.0;
    let pFailure = 0;
    for (let r = numParityShards + 1; r <= numDataShards + numParityShards; r++) {
        const prYear = choose(numDataShards + numParityShards, r) * Math.pow(afr, r) * Math.pow(1 - afr, numDataShards + numParityShards - r);
        const prRebuild = prYear * Math.pow(rebuildTime / yr, r - 1);
        pFailure += prRebuild;
    }
    
    const durability = 1 - pFailure;
    const numFailuresPerYear = 1 - durability;
    let numNines;
    if (numFailuresPerYear === 0) {
        numNines = 'Infinite';
    } else {
        numNines = -Math.log10(numFailuresPerYear);
    }

    const expectedLostObjectsPerYear = totalObjects * numFailuresPerYear;
    
    document.getElementById('output').innerHTML = 
        `The calculated durability is: ${(durability * 100).toFixed(15)}%<br>
         The number of nines in the durability is: ${numNines}<br>
         The expected number of objects lost per year is: ${expectedLostObjectsPerYear}`;
}
