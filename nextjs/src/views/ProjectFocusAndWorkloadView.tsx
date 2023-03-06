import { Segmented } from "antd";
import { FC } from "react";
import { AiFillProject, AiFillSliders } from "react-icons/ai";

interface IProps {
  className?: string
}

const segmentList = [
  {
    label: "Special/Focused Project",
    value: 0,
    icon: <AiFillProject/>
  },
  {
    label: "Workload",
    value: 1,
    icon: <AiFillSliders/>
  }
]

const ProjectFocusAndWorkloadView: FC<IProps> = ({ className }) => {
  const parentClass = className ?? ''
  return (
    <div className={`${className}`}>
      <Segmented options={segmentList}/>
    </div>
  )
}

export default ProjectFocusAndWorkloadView
