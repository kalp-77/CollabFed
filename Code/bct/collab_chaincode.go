package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

type Request struct {
	RequestID   string `json:"requestId"`
	Consumer    string `json:"consumer"`
	VMSpecs     string `json:"vmSpecs"`
	Duration    int    `json:"duration"`
	BlockNumber int    `json:"blockNumber"`
	Offset      int    `json:"offset"`
}

type Endorsement struct {
	RequestID string `json:"requestId"`
	Count     int    `json:"count"`
	Signers   []string `json:"signers"`
}

func (s *SmartContract) SubmitEndorsement(ctx contractapi.TransactionContextInterface, requestId, signer string) error {
	endorsementBytes, _ := ctx.GetStub().GetState(requestId)
	var endorsement Endorsement
	if endorsementBytes == nil {
		endorsement = Endorsement{RequestID: requestId, Count: 1, Signers: []string{signer}}
	} else {
		json.Unmarshal(endorsementBytes, &endorsement)
		endorsement.Count++
		endorsement.Signers = append(endorsement.Signers, signer)
	}
	
	if endorsement.Count > (2 * 3 / 3) { // Assuming 3 CSPs for simplicity
		// Mark request as approved
	}
	
	endorsementBytes, _ = json.Marshal(endorsement)
	return ctx.GetStub().PutState(requestId, endorsementBytes)
}

type SchedulingResult struct {
	RequestID string `json:"requestId"`
	CSP       string `json:"csp"`
}

func (s *SmartContract) FairSchedule(ctx contractapi.TransactionContextInterface, requestId string, contributions map[string]float64, window []SchedulingResult) (string, error) {
	// Implement Algorithm 1 from the paper
	deficits := make(map[string]float64)
	for csp := range contributions {
		deficits[csp] = contributions[csp]
		for _, result := range window {
			if result.CSP == csp {
				deficits[csp] -= 1.0 / float64(len(window))
			}
		}
	}
	
	// Find CSP with maximum deficit
	maxDeficitCSP := ""
	maxDeficit := -1.0
	for csp, deficit := range deficits {
		if deficit > maxDeficit {
			maxDeficit = deficit
			maxDeficitCSP = csp
		}
	}
	
	result := SchedulingResult{RequestID: requestId, CSP: maxDeficitCSP}
	resultBytes, _ := json.Marshal(result)
	ctx.GetStub().PutState(requestId+"_result", resultBytes)
	
	return maxDeficitCSP, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		fmt.Printf("Error creating chaincode: %v", err)
	}
	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %v", err)
	}
}
