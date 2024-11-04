import { Component, OnInit } from '@angular/core';
import { ChartConfiguration } from 'chart.js/auto';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {
  constructor() { }

  public data: ChartConfiguration<'line'>['data'] = {
    datasets: [
      {
        label: "Sales",
        data: [467, 576, 572, 79, 92, 574, 573, 576],
        backgroundColor: 'blue'
      },
    ]
  };

  public chartType: ChartConfiguration<'line'>['type'] = 'line';

  public chartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: !false,
  };

  public chartPlugins = [];

  ngOnInit(): void {
    // this.createChart();
  }

  public chart: any;

  createChart(): void {
    this.data = {
      datasets: [
        {
          label: "Sales",
          data: [467, 576, 572, 79, 92, 574, 573, 576],
          backgroundColor: 'blue'
        },
      ]
    } as ChartConfiguration<'line'>['data'];
  }
}