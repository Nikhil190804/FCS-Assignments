/*
PART A
*/

const FILE_SYSTEM = require('fs')
const DNS = require("dns");
const { promisify } = require("util");
const resolve4Async = promisify(DNS.resolve4);

const CRTSH_URL = "https://crt.sh/?q="
const DNSDUMPSTER_URL = "https://api.dnsdumpster.com/domain/"
const SEARCH_QUERY = "iiitd.edu.in"

const getIP = async (domain_name) => {
    try {
        const addresses = await resolve4Async(domain_name);
        if(addresses.length >=1){
            return addresses[0];
        }
        else{
            return -1;
        }
    } catch (err) {
        return -1;
    }
};


let crt_data = FILE_SYSTEM.readFileSync("crtsh.json","utf-8")
crt_data = JSON.parse(crt_data)

let dnsdumpster_data = FILE_SYSTEM.readFileSync("dnsdumpster.json")
dnsdumpster_data = JSON.parse(dnsdumpster_data)["a"]


let DOMAIN_NAME_TO_IP_MAPPING = []


const process_crt_data = async (crt_data,DOMAIN_NAME_TO_IP_MAPPING)=>{
    for(let i=0;i<crt_data.length;i++){
        let domain_name = crt_data[i]["common_name"]
        let ip = await getIP(domain_name)
        if(ip==-1){
            //console.log(`IP Not found for domain name: ${domain_name} `);
        }
        else{
            DOMAIN_NAME_TO_IP_MAPPING.push([domain_name,ip])
        }
    }

}


const process_dnsdumpster_data = async (dnsdumpster_data,DOMAIN_NAME_TO_IP_MAPPING)=>{
    for(let i=0;i<dnsdumpster_data.length;i++){
        let domain_name = dnsdumpster_data[i]["host"]
        let ip = await getIP(domain_name)
        if(ip==-1){
            //console.log(`IP Not found for domain name: ${domain_name} `);
        }
        else{
            DOMAIN_NAME_TO_IP_MAPPING.push([domain_name,ip])
        }
    }

}



(async ()=>{
    DOMAIN_NAME_TO_IP_MAPPING.push(["Domain Name","IP"])
    await process_crt_data(crt_data,DOMAIN_NAME_TO_IP_MAPPING);
    await process_dnsdumpster_data(dnsdumpster_data,DOMAIN_NAME_TO_IP_MAPPING);
    const csv_data = DOMAIN_NAME_TO_IP_MAPPING.map(row =>{
       return row.join(",")
    }).join("\n");
    FILE_SYSTEM.writeFileSync("DOMAIN_TO_IP.csv",csv_data)
    console.log("Domain name and IP address saved to DOMAIN_TO_IP.csv");
    console.log("Part A Answer:-");
    
    for(let i=0;i<DOMAIN_NAME_TO_IP_MAPPING.length-1000;i++){
        console.log(`${DOMAIN_NAME_TO_IP_MAPPING[i][0]} : ${DOMAIN_NAME_TO_IP_MAPPING[i][1]}`);
    }
    
});


/**
PART B
*/



async function automate_crtsh(){
    const url = CRTSH_URL+SEARCH_QUERY+"&output=json"
    const api_hit = await fetch(url);
    if(!api_hit.ok){
        console.log(`Error in HTTP!\nResponse Code is: ${api_hit.status}`);
        return;
    }
    const data = await api_hit.json();
    //console.log(data);
    let crt_data = []
    crt_data.push(["Domain Name","IP"])
    await process_crt_data(data,crt_data)
    const csv_data = crt_data.map(row =>{
        return row.join(",")
     }).join("\n");
     FILE_SYSTEM.writeFileSync("AUTOMATED_CRTSH_DOMAIN_TO_IP.csv",csv_data)
     console.log("Automation of CRT.SH DONE!!\nDomain name and IP address saved to AUTOMATED_CRTSH_DOMAIN_TO_IP.csv");
    
}
automate_crtsh()



async function automate_dnsdumpster(){
    const url = DNSDUMPSTER_URL+SEARCH_QUERY
    const DNSDUMPSTER_API_KEY = "a6ab3fc629f4501aa7f26dc412fe243057b99688d3f18aa3e332438fc5852e26"
    const api_hit = await fetch(url, {
        method: "GET",
        headers: {
            "X-API-KEY": DNSDUMPSTER_API_KEY,
            "Accept": "application/json"
        }
    });
    if(!api_hit.ok){
        console.log(`Error in HTTP!\nResponse Code is: ${api_hit.status}`);
        return;
    }
    let data = await api_hit.json();
    data = data["a"]
    let dns_dumpster_data = []
    dns_dumpster_data.push(["Domain Name","IP"])
    await process_dnsdumpster_data(data,dns_dumpster_data)
    const csv_data = dns_dumpster_data.map(row =>{
        return row.join(",")
     }).join("\n");
     FILE_SYSTEM.writeFileSync("AUTOMATED_DNSDUMPSTER_DOMAIN_TO_IP.csv",csv_data)
     console.log("Automation of DNSDUMPSTER DONE!!\nDomain name and IP address saved to AUTOMATED_DNSDUMPSTER_DOMAIN_TO_IP.csv");

}
automate_dnsdumpster()