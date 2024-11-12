### 环境部署说明
1. 该系统是使用python语言和django框架进行开发的，请事先安装好python语言
2. 该系统使用的数据库类型为MySQL，请事先安装好MySQL数据库，为保障系统兼容，版本至少8以上
3. 必需依赖文件列表详情见requirements.txt，请全部安装
4. 所有环境搭建完成后，可尝试在 Windows 环境下启动主目录中的startup.cmd
5. 若系统成功监听5200端口，则证明系统已启动
6. 随后请在数据库中执行下列sql语句：
    ```sql
   DROP TABLE IF EXISTS `index_article`;
    CREATE TABLE `index_article`  (
    `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    `term` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    `df` int(0) NULL DEFAULT NULL,
    `docs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    PRIMARY KEY (`id`) USING BTREE,
    INDEX `term`(`term`(768)) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

    SET FOREIGN_KEY_CHECKS = 1; 
7. sql成功执行后，那么恭喜你，系统环境已经成功部署，该系统可以正常使用了


### Environment Deployment Instructions
1. The system is developed using python language and django framework, please install python language in advance
2. The database type used by the system is MySQL. Please install the MySQL database in advance. To ensure system compatibility, the version must be at least 8 or above
3. For the list of required dependent files, see requirements.txt for details, please install them all
4. After all the environments are set up, you can try to start startup.cmd in the main directory in the Windows environment
5. If the system successfully listens to port 5200, it proves that the system has started
6. Then please execute the following sql statement in the database:
     ```sql
    DROP TABLE IF EXISTS `index_article`;
     CREATE TABLE `index_article` (
     `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
     `term` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
     `df` int(0) NULL DEFAULT NULL,
     `docs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
     PRIMARY KEY (`id`) USING BTREE,
     INDEX `term`(`term`(768)) USING BTREE
     ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

     SET FOREIGN_KEY_CHECKS = 1;
7. After the sql is successfully executed, congratulations, the system environment has been successfully deployed, and the system can be used normally