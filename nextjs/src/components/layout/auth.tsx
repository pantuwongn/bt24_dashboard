import { useUserStore } from "@/store/user.store"
import { Avatar } from "antd"
import { FC } from "react"
import { AiOutlineUser } from "react-icons/ai"

interface IProps {
  className?: string
}

const AuthSection: FC<IProps> = ({ className }: IProps) => {
  const {
    user
  } = useUserStore()

  const parentClass = className ?? ''
  return (
    <div className={`flex items-center ${parentClass}`}>
      <Avatar size={"default"} icon={<AiOutlineUser/>}/>
      <div className="mx-4">{ user.name }</div>
    </div>
  )
}

export default AuthSection
