import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";

@Component({
  selector: "dfx-list-item",
  templateUrl: "./list-item.component.html",
  styleUrls: ["./list-item.component.css"],
})
export class ListItemComponent implements OnInit {
  @Input() node;

  @Output() removeItem: EventEmitter<any> = new EventEmitter<any>();

  constructor() {}

  ngOnInit() {}

  remove() {
    this.removeItem.emit(true);
  }
}
