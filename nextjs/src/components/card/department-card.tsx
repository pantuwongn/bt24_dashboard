import { FC } from "react";
import { Department } from "@/types/organization";
import { Avatar, Card } from "antd";
import { AiOutlineUser } from "react-icons/ai";

interface IProps {
  department: Department
  isSelected: boolean
  onClick: (department: Department) => void
}

const { Meta } = Card

const DepartmentCard: FC<IProps> = ({ department, isSelected, onClick }) => {
  const name = department.dep_name
  const head = department.dep_head_name
  const position = department.dep_head_pos

  let baseCardClass = 'my-1'
  baseCardClass += (isSelected ? ' bg-blue-100' : ' bg-white')
  return (
    <Card
      hoverable
      className={baseCardClass}
      style={{ width: 220 }}
      onClick={() => onClick(department)}>
      <Meta
        avatar={<Avatar size={"large"} icon={<AiOutlineUser />} />}
        title={
          <>
            <div className="font-bold">{name}</div>
            <div className="font-normal">{head}</div>
            <div className="font-light">{`<${position}>`}</div>
          </>
        } />
    </Card>
  )
}

export default DepartmentCard