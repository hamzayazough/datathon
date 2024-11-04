import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss'],
})
export class GraphComponent implements OnInit {
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;
  @Input() data: any;

  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [],
    datasets: [
      {
        data: [],
        label: 'Close price',
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Price',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Month',
        },
      },
    },
  };

  public lineChartType: ChartConfiguration<'line'>['type'] = 'line';

  constructor() {}

  ngOnInit(): void {
    this.data.subscribe((res: any) => {
      console.log(res.Close);
      this.updateChartData(Object.values(res.Close), Object.keys(res.Close));
      this.updateChart();
    });
  }

  private updateChart(): void {
    if (this.chart?.chart) {
      this.chart.chart.update();
    }
  }

  // Optional: Method to update data dynamically
  public updateChartData(newData: number[], newKeys: string[]): void {
    console.log(newData);
    this.lineChartData.labels = newKeys.map((x) =>
      new Date(parseInt(x)).toLocaleDateString()
    );
    this.lineChartData.datasets[0].data = newData;
    this.updateChart();
  }
}
