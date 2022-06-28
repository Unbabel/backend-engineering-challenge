package com.unbabel.translationDelivery.listener;

import com.unbabel.translationDelivery.config.BatchConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.listener.JobExecutionListenerSupport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

public class JobListener extends JobExecutionListenerSupport {

    private static final Logger LOG = LoggerFactory.getLogger(BatchConfig.class);

    @Override
    public void afterJob(JobExecution jobExecution) {
        if (jobExecution.getStatus() == BatchStatus.COMPLETED) {
            LOG.info("JOB COMPLETED SUCCESSFULLY");
        } else {
            LOG.error("JOB ended whit status: " + jobExecution.getStatus());
        }
    }

    /**
     * Before Job executes
     * @param jobExecution
     */
    @Override
    public void beforeJob(JobExecution jobExecution) {
        //Auto-generated method stub
        super.beforeJob(jobExecution);
    }
}
