import { Component, OnInit, Input, ElementRef } from "@angular/core";
import { Node } from "../models/node.model";

import { FormControl } from "@angular/forms";

@Component({
  selector: "dfx-list",
  templateUrl: "./list.component.html",
  styleUrls: ["./list.component.css"],
})
export class ListComponent implements OnInit {
  @Input() data: Node[];
  newItem: boolean = false;
  itemForm: FormControl = new FormControl();
  impactForm: FormControl = new FormControl();
  detectedForm: FormControl = new FormControl();
  affectedForm: FormControl = new FormControl();
  recommendationForm: FormControl = new FormControl();

  constructor() {}

  ngOnInit() {}

  submit() {
    this.newItem = false;
    this.data.push({
      item: this.itemForm.value,
      type: "threat",
      detected: [],
      affected: [],
      impact: [],
      recommendation: [],
    });
    this.itemForm.setValue("");
  }

  submitImpact(index, node) {
    node.impact.new = false;
    if (this.hasCharacter(this.impactForm.value)) {
      this.data[index].impact.push({
        item: this.impactForm.value,
      });
    }
    this.impactForm.setValue("");
  }

  submitDetected(index, node) {
    node.detected.new = false;
    if (this.hasCharacter(this.detectedForm.value)) {
      this.data[index].detected.push({
        item: this.detectedForm.value,
      });
    }
    this.detectedForm.setValue("");
  }

  submitAffected(index, node) {
    node.affected.new = false;
    if (this.hasCharacter(this.affectedForm.value)) {
      this.data[index].affected.push({
        item: this.affectedForm.value,
      });
    }
    this.affectedForm.setValue("");
  }

  submitRecommendation(index, node) {
    node.recommendation.new = false;
    if (this.hasCharacter(this.recommendationForm.value)) {
      this.data[index].recommendation.push({
        item: this.recommendationForm.value,
      });
    }
    this.recommendationForm.setValue("");
  }

  remove(index) {
    this.data.splice(index, 1);
  }

  removeItem(array: any[], index) {
    array.splice(index, 1);
  }

  log(e) {
    console.log(e);
  }

  private hasCharacter(value: string): boolean {
    if (value === null) return false;
    const regex = /([a-zA-Z0-9])\w+/g;
    const found = value.match(regex);
    if (found != null) return true;
    return false;
  }
}
