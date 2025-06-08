from .UserSchema import UserSchema, UserCreation, UserResponse, UserUpdate
from .AuthSchema import AuthResponse, LoginUserData
from .RepoSchema import RepoUpdate, RepoCreate, RepoResponse, RepoBase,RepoResponseWithMessage

UserResponse.model_rebuild()
RepoResponse.model_rebuild()