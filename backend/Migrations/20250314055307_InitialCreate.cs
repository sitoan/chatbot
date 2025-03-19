using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace TourFlowBE.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CountryDestination",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Country = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__CountryD__3214EC273AB0E1C6", x => x.ID);
                });

            migrationBuilder.CreateTable(
                name: "TourflowUser",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Email = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    TourflowUserName = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    isAdmin = table.Column<bool>(type: "bit", nullable: true, defaultValue: false),
                    JWT = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                    RefreshKey = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                    AvatarUrl = table.Column<string>(type: "varchar(1000)", unicode: false, maxLength: 1000, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__Tourflow__3214EC2764F2F9E4", x => x.ID);
                });

            migrationBuilder.CreateTable(
                name: "CityDestination",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    City = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    CountryDestinationID = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__CityDest__3214EC279EEB85A6", x => x.ID);
                    table.ForeignKey(
                        name: "FK_CountryDestination",
                        column: x => x.CountryDestinationID,
                        principalTable: "CountryDestination",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "User_DataCollection",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    UserID = table.Column<int>(type: "int", nullable: true),
                    PhoneNumber = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true),
                    TourID = table.Column<int>(type: "int", nullable: true),
                    StarPos = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    EndPos = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    StartDate = table.Column<DateOnly>(type: "date", nullable: true),
                    Duration = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Budget = table.Column<double>(type: "float", nullable: true),
                    AvailableSlot = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__User_Dat__3214EC2795DB0931", x => x.ID);
                    table.ForeignKey(
                        name: "FK_USerDataCollection",
                        column: x => x.UserID,
                        principalTable: "TourflowUser",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "IMGs",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CityDestinationID = table.Column<int>(type: "int", nullable: true),
                    Url = table.Column<string>(type: "varchar(1000)", unicode: false, maxLength: 1000, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__IMGs__3214EC270676CB0B", x => x.ID);
                    table.ForeignKey(
                        name: "FK_IMGsTourID",
                        column: x => x.CityDestinationID,
                        principalTable: "CityDestination",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Tour",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CityDestinationID = table.Column<int>(type: "int", nullable: true),
                    DepartureLocation = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    StartDate = table.Column<DateTime>(type: "datetime", nullable: true),
                    EndDate = table.Column<DateTime>(type: "datetime", nullable: true),
                    Price = table.Column<double>(type: "float", nullable: true),
                    AvailableSlots = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__Tour__3214EC2728815A36", x => x.ID);
                    table.ForeignKey(
                        name: "FK_TourID",
                        column: x => x.CityDestinationID,
                        principalTable: "CityDestination",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "TourOrder",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BookDate = table.Column<DateTime>(type: "datetime", nullable: true),
                    TourflowUserID = table.Column<int>(type: "int", nullable: false),
                    TourBooked = table.Column<int>(type: "int", nullable: false),
                    Slots = table.Column<int>(type: "int", nullable: true),
                    TotalPrice = table.Column<double>(type: "float", nullable: true),
                    Paid = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__TourOrde__3214EC2712660D55", x => x.ID);
                    table.ForeignKey(
                        name: "FK_BookedTourID",
                        column: x => x.TourBooked,
                        principalTable: "Tour",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_TourflowUserID",
                        column: x => x.TourflowUserID,
                        principalTable: "TourflowUser",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "TourPlan",
                columns: table => new
                {
                    ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    TourID = table.Column<int>(type: "int", nullable: true),
                    Detail = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__TourPlan__3214EC275A643148", x => x.ID);
                    table.ForeignKey(
                        name: "FK_TourPlanID",
                        column: x => x.TourID,
                        principalTable: "Tour",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CityDestination_CountryDestinationID",
                table: "CityDestination",
                column: "CountryDestinationID");

            migrationBuilder.CreateIndex(
                name: "IX_IMGs_CityDestinationID",
                table: "IMGs",
                column: "CityDestinationID");

            migrationBuilder.CreateIndex(
                name: "IX_Tour_CityDestinationID",
                table: "Tour",
                column: "CityDestinationID");

            migrationBuilder.CreateIndex(
                name: "IX_TourOrder_TourBooked",
                table: "TourOrder",
                column: "TourBooked");

            migrationBuilder.CreateIndex(
                name: "IX_TourOrder_TourflowUserID",
                table: "TourOrder",
                column: "TourflowUserID");

            migrationBuilder.CreateIndex(
                name: "IX_TourPlan_TourID",
                table: "TourPlan",
                column: "TourID");

            migrationBuilder.CreateIndex(
                name: "IX_User_DataCollection_UserID",
                table: "User_DataCollection",
                column: "UserID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "IMGs");

            migrationBuilder.DropTable(
                name: "TourOrder");

            migrationBuilder.DropTable(
                name: "TourPlan");

            migrationBuilder.DropTable(
                name: "User_DataCollection");

            migrationBuilder.DropTable(
                name: "Tour");

            migrationBuilder.DropTable(
                name: "TourflowUser");

            migrationBuilder.DropTable(
                name: "CityDestination");

            migrationBuilder.DropTable(
                name: "CountryDestination");
        }
    }
}
