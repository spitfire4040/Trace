// HEADER FILES
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

// MAIN FUNCTION
int main(int argc, char *argv[])
{
	// initialize variables
	time_t e_time;
	int year, month, day, duration, ripeYear, ripeMonth, ripeDay, arkYear, arkMonth, arkDay, sleep = 0;
	int mlabMonth, mlabYear, mlabDay, iplaneMonth, iplaneYear, iplaneDay;
	bool yearflag = false, monthflag = false, dayflag = false;
	char y[4];
	char m[2];
	char d[2];
	char e[12];
	char temp[3];
	char et[11];
	char ripeparams[40];
	char arkparams[40];
	char mlabparams[40];
	char iplaneparams[40];
	char* zero = "0";

	// outfile pointers
	FILE* outfile1;
	FILE* outfile2;

	// create struct for time
	struct tm t;

	// prompt for date:
	// year
	while (yearflag == false)
	{
		system("clear");
		printf("Enter desired year as an integer value between 2010 and 2016: ");
		scanf("%d", &year);

		// check for good input
		if((year >= 2010) && (year <= 2016))
		{
			yearflag = true;
		}
	}

	// month
	while(monthflag == false)
	{
		system ("clear");
		printf ("Enter desired month as an integer value between 1 and 12: ");
		scanf ("%d", &month);

		// check for good input
		if((month >= 1) && (month <= 12))
		{
			monthflag = true;
		}
	}

	// day
	while(dayflag == false)
	{
		system("clear");
		printf("Enter desired day as an integer value between 1 and 31: ");
		scanf("%d", &day);

		// check for good input
		if((day >= 1) && (day <= 31))
		{
			dayflag = true;
		}		
	}

	// duration
	system("clear");
	printf("Enter number of days to run (default is 1): ");
	scanf("%d", &duration);

	if(duration < 1 || duration > 62)
	{
		duration = 1;
	}

	// run ripe

	ripeYear = year;
	ripeMonth = month;
	ripeDay = day;

	for(int x = 0; x < duration; x++)
	{
		if(x > 0)
		{
			// increment year for each iteration
			if(ripeMonth == 12 && ripeDay == 31)
			{
				ripeYear += 1;
			}

			// increment day for each iteration
			// for February...
			if(ripeMonth == 2)
			{
				if(ripeDay < 28)
				{
					ripeDay += 1;
				}
				else
				{
					ripeDay = 1;

					// increment month for each iteration
					if(ripeMonth < 12)
					{
						ripeMonth += 1;
					}
					else
					{
						ripeMonth = 1;
					}
				}

			}
			// for months with 31 days...
			else if(ripeMonth == 1 || ripeMonth == 3 || ripeMonth == 5 || ripeMonth == 7 || ripeMonth == 8 || ripeMonth == 10 || ripeMonth == 12)
			{
				if(ripeDay < 31)
				{
					ripeDay += 1;
				}
				else
				{
					ripeDay = 1;

					// increment month for each iteration
					if(ripeMonth < 12)
					{
						ripeMonth += 1;
					}
					else
					{
						ripeMonth = 1;
					}
				}
			}
			// for months with 30 days...
			else
			{
				if(ripeDay < 30)
				{
					ripeDay += 1;
				}
				else
				{
					ripeDay = 1;

					// increment month for each iteration
					if(ripeMonth < 12)
					{
						ripeMonth += 1;
					}
					else
					{
						ripeMonth = 1;
					}
				}
			}
		}

		// convert to unix epoch time
		t.tm_year = (ripeYear - 1900);
		t.tm_mon = (ripeMonth - 1);
		t.tm_mday = ripeDay;
		t.tm_hour = 8;
		t.tm_min = 00;
		t.tm_sec = 00;
		t.tm_isdst = 0;
		e_time = mktime (&t);
		sprintf(e, "%ld", e_time);

		// call ripe
		strcpy(ripeparams, "python3.5 ripe_day.py ");
		strcat(ripeparams, e);
		system(ripeparams);
		//printf("Ripe: %s\n", ripeparams);

	}


	// call ark

	arkYear = year;
	arkMonth = month;
	arkDay = day;

	for(int x = 0; x < duration; x++)
	{
		if(x > 0)
		{
			// increment year for each iteration
			if(arkMonth == 12 && arkDay == 31)
			{
				arkYear += 1;
			}



			// increment day for each iteration
			// for February...
			if(arkMonth == 2)
			{
				if(arkDay < 28)
				{
					arkDay += 1;
				}
				else
				{
					arkDay = 1;

					// increment month for each iteration
					if(arkMonth < 12)
					{
						arkMonth += 1;
					}
					else
					{
						arkMonth = 1;
					}					
				}

			}
			// for months with 31 days...
			else if(arkMonth == 1 || arkMonth == 3 || arkMonth == 5 || arkMonth == 7 || arkMonth == 8 || arkMonth == 10 || arkMonth == 12)
			{
				if(arkDay < 31)
				{
					arkDay += 1;
				}
				else
				{
					arkDay = 1;

					// increment month for each iteration
					if(arkMonth < 12)
					{
						arkMonth += 1;
					}
					else
					{
						arkMonth = 1;
					}
				}
			}
			// for months with 30 days...
			else
			{
				if(arkDay < 30)
				{
					arkDay += 1;
				}
				else
				{
					arkDay = 1;

					// increment month for each iteration
					if(arkMonth < 12)
					{
						arkMonth += 1;
					}
					else
					{
						arkMonth = 1;
					}
				}
			}
		}

		// convert year to string
		sprintf(y, "%d", arkYear);

		// correct for 1 digit month
		if(month < 10)
		{
			strcpy(m, zero);
			sprintf(temp, "%d", arkMonth);
			strcat(m, temp);
		}

		else
		{
			sprintf(m, "%d", arkMonth);
		}

		// correct for 1 digit day
		if(arkDay < 10)
		{
			strcpy(d, zero);
			sprintf(temp, "%d", arkDay);
			strcat(d, temp);
		}

		else
		{
			sprintf(d, "%d", arkDay);
		}

		// build string for parameter
		strcpy(arkparams, "python3.5 arkparse.py ");
		strcat(arkparams, y);
		strcat(arkparams, " ");
		strcat(arkparams, m);
		strcat(arkparams, " ");
		strcat(arkparams, d);
		system(arkparams);
		//printf("Ark: %s\n", arkparams);
	}


	// call mlab
	mlabYear = year;
	mlabMonth = month;
	mlabDay = day;

	for(int x = 0; x < duration; x++)
	{
		if(x > 0)
		{
			// increment year for each iteration
			if(mlabMonth == 12 && mlabDay == 31)
			{
				mlabYear += 1;
			}



			// increment day for each iteration
			// for February...
			if(mlabMonth == 2)
			{
				if(mlabDay < 28)
				{
					mlabDay += 1;
				}
				else
				{
					mlabDay = 1;

					// increment month for each iteration
					if(mlabMonth < 12)
					{
						mlabMonth += 1;
					}
					else
					{
						mlabMonth = 1;
					}					
				}

			}
			// for months with 31 days...
			else if(mlabMonth == 1 || mlabMonth == 3 || mlabMonth == 5 || mlabMonth == 7 || mlabMonth == 8 || mlabMonth == 10 || mlabMonth == 12)
			{
				if(mlabDay < 31)
				{
					mlabDay += 1;
				}
				else
				{
					mlabDay = 1;

					// increment month for each iteration
					if(mlabMonth < 12)
					{
						mlabMonth += 1;
					}
					else
					{
						mlabMonth = 1;
					}
				}
			}
			// for months with 30 days...
			else
			{
				if(mlabDay < 30)
				{
					mlabDay += 1;
				}
				else
				{
					mlabDay = 1;

					// increment month for each iteration
					if(mlabMonth < 12)
					{
						mlabMonth += 1;
					}
					else
					{
						mlabMonth = 1;
					}
				}
			}
		}

		// convert year to string
		sprintf(y, "%d", mlabYear);

		// correct for 1 digit month
		if(month < 10)
		{
			strcpy(m, zero);
			sprintf(temp, "%d", mlabMonth);
			strcat(m, temp);
		}

		else
		{
			sprintf(m, "%d", mlabMonth);
		}

		// correct for 1 digit day
		if(mlabDay < 10)
		{
			strcpy(d, zero);
			sprintf(temp, "%d", mlabDay);
			strcat(d, temp);
		}

		else
		{
			sprintf(d, "%d", mlabDay);
		}

		// build string for parameter
		strcpy(mlabparams, "python3.5 mlab.py ");
		strcat(mlabparams, y);
		strcat(mlabparams, " ");
		strcat(mlabparams, m);
		strcat(mlabparams, " ");
		strcat(mlabparams, d);
		system(mlabparams);
		//printf("M-lab: %s\n", mlabparams);
	}
	

	// call iplane
	iplaneYear = year;
	iplaneMonth = month;
	iplaneDay = day;

	for(int x = 0; x < duration; x++)
	{
		if(x > 0)
		{
			// increment year for each iteration
			if(iplaneMonth == 12 && iplaneDay == 31)
			{
				iplaneYear += 1;
			}



			// increment day for each iteration
			// for February...
			if(iplaneMonth == 2)
			{
				if(iplaneDay < 28)
				{
					iplaneDay += 1;
				}
				else
				{
					iplaneDay = 1;

					// increment month for each iteration
					if(iplaneMonth < 12)
					{
						iplaneMonth += 1;
					}
					else
					{
						iplaneMonth = 1;
					}					
				}

			}
			// for months with 31 days...
			else if(iplaneMonth == 1 || iplaneMonth == 3 || iplaneMonth == 5 || iplaneMonth == 7 || iplaneMonth == 8 || iplaneMonth == 10 || iplaneMonth == 12)
			{
				if(iplaneDay < 31)
				{
					iplaneDay += 1;
				}
				else
				{
					iplaneDay = 1;

					// increment month for each iteration
					if(iplaneMonth < 12)
					{
						iplaneMonth += 1;
					}
					else
					{
						iplaneMonth = 1;
					}
				}
			}
			// for months with 30 days...
			else
			{
				if(iplaneDay < 30)
				{
					iplaneDay += 1;
				}
				else
				{
					iplaneDay = 1;

					// increment month for each iteration
					if(iplaneMonth < 12)
					{
						iplaneMonth += 1;
					}
					else
					{
						iplaneMonth = 1;
					}
				}
			}
		}

		// convert year to string
		sprintf(y, "%d", iplaneYear);

		// correct for 1 digit month
		if(month < 10)
		{
			strcpy(m, zero);
			sprintf(temp, "%d", iplaneMonth);
			strcat(m, temp);
		}

		else
		{
			sprintf(m, "%d", iplaneMonth);
		}

		// correct for 1 digit day
		if(iplaneDay < 10)
		{
			strcpy(d, zero);
			sprintf(temp, "%d", iplaneDay);
			strcat(d, temp);
		}

		else
		{
			sprintf(d, "%d", iplaneDay);
		}

		// build string for parameter
		strcpy(iplaneparams, "python iplane_trace.py ");
		strcat(iplaneparams, y);
		strcat(iplaneparams, " ");
		strcat(iplaneparams, m);
		strcat(iplaneparams, " ");
		strcat(iplaneparams, d);
		system(iplaneparams);
		//printf("iPlane: %s\n", iplaneparams);
	}

	// end program
	return 0;
}

