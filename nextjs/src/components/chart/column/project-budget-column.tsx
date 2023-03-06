import { FC } from "react"
import { ColumnConfig } from "@ant-design/charts"
import dynamic from "next/dynamic"

const Column = dynamic(() => import("@ant-design/charts").then((m) => m.Column), { ssr: false })

interface IProps { }

const data: Record<string, any>[] = [
  {
    name: 'Plan',
    plan: 'FY',
    actual: 3,
  },
  {
    name: 'Plan',
    plan: '1st',
    actual: 5,
  },
  {
    name: 'Plan',
    plan: '2nd',
    actual: 2,
  },
  {
    name: 'Plan',
    plan: 'Month',
    actual: 1,
  },
  {
    name: 'Actual',
    plan: 'FY',
    actual: 2.4,
  },
  {
    name: 'Actual',
    plan: '1st',
    actual: 3.2,
  },
  {
    name: 'Actual',
    plan: '2nd',
    actual: 4.2,
  },
  {
    name: 'Actual',
    plan: 'Month',
    actual: 3.9,
  },
]

const config: ColumnConfig = {
  data,
  isGroup: true,
  xField: 'plan',
  yField: 'actual',
  seriesField: 'name',
  color: ['#1ca9e6', '#f88c24'],
  marginRatio: 0.1,
  width: 180,
  height: 180,
  label: {
    position: 'middle',
    layout: [
      {
        type: 'interval-adjust-position',
      },
      {
        type: 'interval-hide-overlap',
      },
      {
        type: 'adjust-color',
      },
    ],
  },
}

const ProjectBudgetColumnChart: FC<IProps> = () => {
  return (
    <Column {...config} />
  )
}

export default ProjectBudgetColumnChart
